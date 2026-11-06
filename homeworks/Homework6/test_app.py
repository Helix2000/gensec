import importlib.util
import pathlib
import unittest
from unittest.mock import MagicMock, patch


APP_PATH = pathlib.Path(__file__).with_name("app.py")
spec = importlib.util.spec_from_file_location("homework6_app", APP_PATH)
app = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(app)


class TestPortScanner(unittest.TestCase):
    def test_parse_port_range_valid(self):
        self.assertEqual(app.parse_port_range("20-80"), (20, 80))

    def test_parse_port_range_invalid_input(self):
        with self.assertRaises(ValueError):
            app.parse_port_range("abc")

    def test_parse_port_range_negative_ports(self):
        with self.assertRaises(ValueError):
            app.parse_port_range("-1-10")

    def test_parse_port_range_reversed(self):
        with self.assertRaises(ValueError):
            app.parse_port_range("80-20")

    def test_parse_port_number_negative(self):
        with self.assertRaises(ValueError):
            app.parse_port_number("-5")

    def test_resolve_loopback_rejects_external_ip(self):
        with self.assertRaises(ValueError):
            app.resolve_loopback_addresses("8.8.8.8")

    @patch.object(app.socket, "getaddrinfo")
    def test_resolve_loopback_accepts_localhost(self, mock_getaddrinfo):
        mock_getaddrinfo.return_value = [
            (app.socket.AF_INET, app.socket.SOCK_STREAM, 6, "", ("127.0.0.1", 0))
        ]

        infos = app.resolve_loopback_addresses("localhost")
        self.assertEqual(len(infos), 1)
        self.assertEqual(infos[0][4][0], "127.0.0.1")

    @patch.object(app.socket, "getaddrinfo")
    def test_resolve_loopback_rejects_non_localhost_hostname(self, mock_getaddrinfo):
        mock_getaddrinfo.return_value = [
            (app.socket.AF_INET, app.socket.SOCK_STREAM, 6, "", ("192.168.1.5", 0))
        ]

        with self.assertRaises(ValueError):
            app.resolve_loopback_addresses("example.local")

    def test_check_tcp_port_open(self):
        infos = [(app.socket.AF_INET, app.socket.SOCK_STREAM, 6, "", ("127.0.0.1", 0))]

        mock_socket = MagicMock()
        mock_socket.connect_ex.return_value = 0

        with patch.object(app.socket, "socket", return_value=mock_socket):
            self.assertTrue(app.check_tcp_port(infos, 80))

    def test_check_tcp_port_closed(self):
        infos = [(app.socket.AF_INET, app.socket.SOCK_STREAM, 6, "", ("127.0.0.1", 0))]

        mock_socket = MagicMock()
        mock_socket.connect_ex.return_value = 1

        with patch.object(app.socket, "socket", return_value=mock_socket):
            self.assertFalse(app.check_tcp_port(infos, 80))


if __name__ == "__main__":
    unittest.main()
