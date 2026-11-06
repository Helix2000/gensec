"""PySecureNetPort - a simple localhost-only TCP port scanner.

This script asks the user for a host (localhost, 127.0.0.1, ::1, or another
hostname that resolves to localhost) and a port range. It then checks each
TCP port and prints whether it is open or closed.
"""

from __future__ import annotations

import ipaddress
import socket
from contextlib import closing
from typing import Any

DEFAULT_TIMEOUT = 0.5
MIN_PORT = 1
MAX_PORT = 65535


def parse_port_number(port_text: str) -> int:
    """Convert one port value to an integer and validate its range."""
    cleaned = port_text.strip()
    if not cleaned:
        raise ValueError("Port numbers cannot be empty.")

    try:
        port = int(cleaned)
    except ValueError as exc:
        raise ValueError("Port numbers must be whole numbers.") from exc

    if port < MIN_PORT or port > MAX_PORT:
        raise ValueError(f"Ports must be between {MIN_PORT} and {MAX_PORT}.")

    return port


def resolve_loopback_addresses(host: str) -> list[tuple[Any, ...]]:
    """Resolve a host and keep only loopback addresses.

    Returns the raw getaddrinfo entries for the host if every resolved address is
    a loopback address. Raises ValueError for invalid or non-local targets.
    """
    cleaned_host = host.strip()
    if not cleaned_host:
        raise ValueError("Host cannot be empty.")

    # If the user entered a direct IP address, reject anything that is not localhost.
    try:
        ip = ipaddress.ip_address(cleaned_host)
    except ValueError:
        ip = None
    else:
        if not ip.is_loopback:
            raise ValueError(
                "Only localhost scanning is allowed. Use localhost, 127.0.0.1, or ::1."
            )
        cleaned_host = str(ip)

    try:
        infos = socket.getaddrinfo(cleaned_host, None, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve host '{host}': {exc}") from exc

    if not infos:
        raise ValueError("No addresses were found for that host.")

    loopback_infos: list[tuple[Any, ...]] = []
    for info in infos:
        family, socktype, proto, canonname, sockaddr = info
        address = sockaddr[0]
        try:
            resolved_ip = ipaddress.ip_address(address)
        except ValueError:
            raise ValueError(
                f"'{host}' resolved to an invalid address: {address}"
            ) from None

        if not resolved_ip.is_loopback:
            raise ValueError(
                "Only localhost scanning is allowed. Use localhost, 127.0.0.1, or ::1."
            )

        loopback_infos.append((family, socktype, proto, canonname, sockaddr))

    return loopback_infos


def parse_port_range(port_range_text: str) -> tuple[int, int]:
    """Parse a port range like '20-80'."""
    cleaned = port_range_text.strip().replace(" ", "")
    parts = cleaned.split("-")
    if len(parts) != 2:
        raise ValueError("Port range must look like start-end, for example 20-80.")

    start_port = parse_port_number(parts[0])
    end_port = parse_port_number(parts[1])

    if start_port > end_port:
        raise ValueError("Start port must be less than or equal to end port.")

    return start_port, end_port


def check_tcp_port(infos: list[tuple], port: int, timeout: float = DEFAULT_TIMEOUT) -> bool:
    """Return True if at least one localhost address accepts the TCP connection."""
    for family, socktype, proto, _, sockaddr in infos:
        try:
            target = (sockaddr[0], port)
            if family == socket.AF_INET6:
                target = (sockaddr[0], port, sockaddr[2], sockaddr[3])

            with closing(socket.socket(family, socktype, proto)) as sock:
                sock.settimeout(timeout)
                if sock.connect_ex(target) == 0:
                    return True
        except OSError:
            # If one address family fails, try the next one.
            continue

    return False


def main() -> None:
    """Run the interactive port scanner."""
    print("PySecureNetPort - localhost TCP port scanner")
    print("Only localhost scanning is allowed.\n")

    try:
        host = input("Enter localhost, 127.0.0.1, ::1, or a hostname that points to localhost: ").strip()
        if not host:
            print("Error: host cannot be empty.")
            return

        start_port, end_port = parse_port_range(input("Enter a port range (start-end): "))
        # Validate the host before scanning any ports.
        resolved_infos = resolve_loopback_addresses(host)
    except (ValueError, EOFError, KeyboardInterrupt) as exc:
        if isinstance(exc, (EOFError, KeyboardInterrupt)):
            print("Error: input was interrupted.")
        else:
            print(f"Error: {exc}")
        return

    print(f"\nScanning {host} from port {start_port} to {end_port}...\n")

    open_ports: list[int] = []
    for port in range(start_port, end_port + 1):
        try:
            is_open = check_tcp_port(resolved_infos, port)
            status = "open" if is_open else "closed"
            print(f"Port {port:5d}: {status}")
            if is_open:
                open_ports.append(port)
        except OSError as exc:
            print(f"Port {port:5d}: error ({exc})")

    print("\nScan complete.")
    if open_ports:
        print("Open ports:", ", ".join(str(port) for port in open_ports))
    else:
        print("No open ports found in that range.")


if __name__ == "__main__":
    main()
