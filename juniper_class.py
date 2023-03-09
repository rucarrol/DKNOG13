"""juniper_class implements BaseDevice methods on Juniper Hardware."""
import re

from antlr4 import *
import base_class
from ISISAdjLexer import ISISAdjLexer
from ISISAdjParser import ISISAdjParser
from textfsm import clitable


class JuniperDevice(BaseClass):

  def __init__(self):
    self.device = None  # Normally, this would be where initialisation happens.

  def fetchFromDevice(self, cmd: str) -> str:
    """A stub/mocked method to fetch output from a device and return it."""
    return ""

  def isUserConfigured(self, username: str) -> bool:
    """Determines if a given user is configured on the device.

    Arguments:
      username: The username to verify.

    Returns:
      If supplied username is configured or not.
    """
    cmd = "show configuration system login"
    user_list_output = self.fetchFromDevice(cmd)
    return f"user {username}" in user_list_output

  def fetchModel(self) -> str:
    """fetchModel fetches the hardware model of a given device.

    Returns:
      The running version of a given device.
    """
    cmd = "show chassis hardware"
    model_re = "((MX|PTX)[0-9]+)"
    model_output = self.fetchFromDevice(cmd)
    return re.search(model_re, model_output, re.MULTILINE).group(0)

  def fetchRunningVersion(self) -> dict:
    """fetchRunningVersion fetches the running version of a given device.

    Returns:
      A dict containing the major, minor, train and build of software
        running.
    """
    version_re = (
        "(?P<major>\d+)"   # Match major version
        + "\."             # Dot seperator
        + "(?P<minor>\d+)" # Match minor version
        + "(?P<train>\w)"  # Match train
        + "(?P<build>\d+)" # Match build
    )
    version_output = self.fetchFromDevice("show version")
    return re.search(version_re, version_output, re.MULTILINE).groupdict()

  def fetchARPTable(self) -> list[list]:
    """Fetches the ARP table.

    Returns:
      A list of lists corresponding to the ARP Table.
    """
    sh_arp_cmd = "show arp no-resolve"
    sh_arp_output = self.fetchFromDevice(sh_arp_cmd)
    cli_table = clitable.CliTable("index", "templates")
    attributes = {"Command": sh_arp_cmd, "Vendor": "Juniper"}
    ret = cli_table.ParseCmd(sh_arp_output, attributes)
    return [list(row) for row in ret]

  def fetchISISAdjacency(self) -> list[dict]:
    """Fetches the ISIS Adjacency table.

    Returns:
      A list of dicts corresponding to the IS-IS neighbours.
    """
    sh_isis_output = self.fetchFromDevice("show isis adjacency")
    tree = _getTree(sh_isis_output)
    return _parseTokens(tree)

  def _getTree(self, output: str) -> ISISAdjParser.InputsContext:
    """_getTree is a helper function which takes input and converts to Tree.

    Arguments:
      output: The output from "show isis adjacency" on a device.

    Returns:
      A tree ready to parse and tokenise the given intput.
    """
    isis_adj = InputStream(output)
    lexer = ISISAdjLexer(isis_adj)
    stream = CommonTokenStream(lexer)
    parser = ISISAdjParser(stream)
    return parser.line()

  def _parseTokens(tree: ISISAdjParser.InputsContext) -> list[dict]:
    """_parseTokens converts a parser tree into a list of dicts.

    Arguments:
      tree: An antlr4 tokensier.

    Returns:
      A list of dicts for each adjacency.
    """
    ret = list()
    for token in tree.getChildren():
      line = {
          "interface": token.Interface().getText(),
          "hostname": token.Hostname().getText(),
          "hold": token.Hold().getText(),
          "level": token.Level().getText(),
      }
      ret.append(line)
    return ret

