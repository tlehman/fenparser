from unittest import TestCase
from itertools import chain
import re

class FenParser():
  def __init__(self, fen_str):
    self.fen_str = fen_str

  def parse(self):
    ranks = self.fen_str.split(" ")[0].split("/")
    pieces_on_all_ranks = [self.parse_rank(rank) for rank in ranks]
    return pieces_on_all_ranks

  def parse_rank(self, rank):
    rank_re = re.compile("(\d|[kqbnrpKQBNRP])")
    piece_tokens = rank_re.findall(rank)
    pieces = self.flatten(map(self.expand_or_noop, piece_tokens))
    return pieces

  def flatten(self, lst):
    return list(chain(*lst))

  def expand_or_noop(self, piece_str):
    piece_re = re.compile("([kqbnrpKQBNRP])")
    retval = ""
    if piece_re.match(piece_str):
      retval = piece_str
    else:
      retval = self.expand(piece_str)
    return retval

  def expand(self, num_str):
    return int(num_str)*" "



class FenParserTest(TestCase):
  def test_parse_rank(self):
    start_pos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    rank8 = "rnbqkbnr"
    rank7 = "pppppppp"
    rank6 = "8"
    fp = FenParser(start_pos)
    assert fp.parse_rank(rank8) == ["r","n","b","q","k","b","n","r"]
    assert fp.parse_rank(rank7) == ["p","p","p","p","p","p","p","p"]
    assert fp.parse_rank(rank6) == [" "," "," "," "," "," "," "," "]


  def test_parse_starting_position(self):
    start_pos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    fp = FenParser(start_pos)
    print fp.parse()
    assert len(fp.parse()) == 8
    assert fp.parse() == [["r","n","b","q","k","b","n","r"],
                          ["p","p","p","p","p","p","p","p"],
                          [" "," "," "," "," "," "," "," "],
                          [" "," "," "," "," "," "," "," "],
                          [" "," "," "," "," "," "," "," "],
                          [" "," "," "," "," "," "," "," "],
                          ["P","P","P","P","P","P","P","P"],
                          ["R","N","B","Q","K","B","N","R"]]
