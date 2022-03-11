####################################################
# You may only change the initial board here       #
# Any change other than board may result in crash  #
####################################################

from gui import App
from PyQt5.QtWidgets import QApplication
import sys
import chess

if __name__ == '__main__':
	app = QApplication(sys.argv)
	board = chess.Board("3K2R1/n3r3/5P1P/8/n7/pp6/kp6/3Q4 b - - 0 1") #initial board is created here
	ex = App(board)
	app.exec_()
