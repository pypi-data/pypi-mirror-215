from __future__ import print_function
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

"""NAPALM Nokia OLT Handler."""
import re
from napalm.base.exceptions import (
    ReplaceConfigException,
    MergeConfigException,
    ConnectionClosedException,
    CommandErrorException,
    CommitConfirmException,
)
from napalm.base.helpers import (
    canonical_interface_name,
    transform_lldp_capab,
    textfsm_extractor,
    split_interface,
    abbreviated_interface_name,
    generate_regex_or,
    sanitize_configs,
)
from napalm.base.netmiko_helpers import netmiko_args
from netmiko import ConnectHandler

import socket
from netmiko import ConnectHandler
from napalm.base.base import NetworkDriver

import xml.etree.ElementTree as ET


# napalm_nokia_olt
class NokiaOltDriver(NetworkDriver):
    """NAPALM Nokia OLT Handler."""

    def __init__(
            self,
            hostname,
            username,
            password,
            timeout=60,
            optional_args=None
    ):
        """Constructor."""
        if optional_args is None:
            optional_args = {}
        self.transport = optional_args.get("transport", "ssh")
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout

        # Netmiko possible arguments
        netmiko_argument_map = {
            'port': None,
            'secret': '',
            'verbose': False,
            'keepalive': 30,
            'global_delay_factor': 1,
            'use_keys': False,
            'key_file': None,
            'ssh_strict': False,
            'system_host_keys': False,
            'alt_host_keys': False,
            'alt_key_file': '',
            'ssh_config_file': None,
            'allow_agent': False,
            'session_log': None,
            "read_timeout_override": 90,  # still monitoring this portion
        }

        # Build dict of any optional Netmiko args
        self.netmiko_optional_args = {}
        for k, v in netmiko_argument_map.items():
            try:
                self.netmiko_optional_args[k] = optional_args[k]
            except KeyError:
                pass

        default_port = {'ssh': 22}
        self.port = optional_args.get('port', default_port[self.transport])
        self.device = None
        self.config_replace = False
        self.interface_map = {}
        self.platform = "cisco_ios"
        self.profile = [self.platform]
        # self.profile = ["sros_isam"] ## TODO:
        # self.device.enable()

    @staticmethod
    def _send_command_postprocess(output):
        """
        Cleanup actions on send_command() for NAPALM getters.
        Remove "Load for five sec; one minute if in output"
        Remove "Time source is"
        """
        output = re.sub(r"^Load for five secs.*$", "", output, flags=re.M)
        output = re.sub(r"^Time source is .*$", "", output, flags=re.M)
        return output.strip()

    def _send_command(self, command):
        """Wrapper for self.device.send.command().
        If command is a list will iterate through commands until valid command.
        """
        try:
            if isinstance(command, list):
                for cmd in command:
                    output = self.device.send_command(cmd)
                    if "% Invalid" not in output:
                        break
            else:
                output = self.device.send_command(command)
                return self._send_command_postprocess(output)
        except (socket.error, EOFError) as e:
            raise ConnectionClosedException(str(e))

    def open(self):
        """Open a connection to the device."""
        device_type = self.platform
        if self.transport == "telnet":
            device_type = f"{self.platform}_telnet"
        self.device = self._netmiko_open(
            device_type, netmiko_optional_args=self.netmiko_optional_args
        )

    def close(self):
        """Close the connection to the device and do the necessary cleanup."""
        self._netmiko_close()

    def is_alive(self):
        """Returns a flag with the state of the connection."""
        null = chr(0)
        if self.device is None:
            return {'is_alive': False}
        else:
            # SSH
            try:
                # Try sending ASCII null byte to maintain the connection alive
                self.device.write_channel(null)
                return {'is_alive': self.device.remote_conn.transport.is_active()}
            except (socket.error, EOFError):
                # If unable to send, we can tell for sure that the connection is unusable
                return {'is_alive': False}


    def get_config(self, retrieve="all", full=False, sanitized=False):
        """
        get_config for sros_isam.
        """
        configs = {
            "running": "",
            "startup": "No Startup",
            "candidate": "No Candidate"
        }

        if retrieve in ("all", "running"):
            command = "info configure"
            output_ = self._send_command(command)
            if output_:
                configs["running"] = output_
                data = str(configs["running"]).split("\n")
                non_empty_lines = [line for line in data if line.strip() != ""]

                string_without_empty_lines = ""
                for line in non_empty_lines:
                    string_without_empty_lines += line + "\n"
                configs["running"] = string_without_empty_lines

        if retrieve.lower() in ("startup", "all"):
            pass
        return configs

