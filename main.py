from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import sys
import spam_form
import analyzer

input_text = ''
is_spam    = False


class Win(QMainWindow):
    def __init__(self):
        QWidget.__init__(self, None)
        self.ui = spam_form.Ui_Form()
        self.ui.setupUi(self)

        self.hide_all()

        self.ui.pushButton_clear.clicked.connect(self.clear_text_field)
        self.ui.pushButton_check.clicked.connect(self.check_spam)
        self.ui.pushButton_true.clicked.connect(self.pressed_true)
        self.ui.pushButton_false.clicked.connect(self.pressed_false)
        self.ui.pushButton_ok.clicked.connect(self.pressed_ok)

    def hide_all(self):
        self.ui.label_prob.clear()
        self.ui.label_cat.clear()
        self.ui.pushButton_true.hide()
        self.ui.pushButton_false.hide()
        self.ui.pushButton_ok.hide()

    def show_all(self):
        self.ui.pushButton_true.setDisabled(False)
        self.ui.pushButton_false.setDisabled(False)
        self.ui.pushButton_true.show()
        self.ui.pushButton_false.show()
        self.ui.pushButton_ok.show()

    def clear_text_field(self):
        self.ui.textEdit.clear()
        self.hide_all()

    def pressed_true(self):
        analyzer.add_study(input_text, is_spam)
        self.ui.pushButton_true.setDisabled(True)
        self.ui.pushButton_false.setDisabled(True)

    def pressed_false(self):
        analyzer.add_study(input_text, not is_spam)
        self.ui.pushButton_true.setDisabled(True)
        self.ui.pushButton_false.setDisabled(True)

    def pressed_ok(self):
        self.ui.pushButton_check.setDisabled(False)
        self.ui.pushButton_clear.setDisabled(False)
        #self.ui.textEdit.setDisabled(False)
        self.clear_text_field()

    def check_spam(self):
        global input_text
        global is_spam

        input_text = self.ui.textEdit.toPlainText()
        if len(input_text.split()) < 3:
            return

        spam_prob = analyzer.nba_spam_predict(input_text)
        is_spam = spam_prob > 0.7

        self.ui.pushButton_check.setDisabled(True)
        self.ui.pushButton_clear.setDisabled(True)
        #self.ui.textEdit.setDisabled(True)
        self.show_all()

        self.ui.label_prob.setText('Вероятность спама %.2f%%' % (spam_prob*100))
        self.ui.label_cat.setText('Введенное сообщение определено как %s' % ('СПАМ' if is_spam else 'НЕ СПАМ'))


analyzer.init()

app = QApplication(sys.argv)
win = Win()
win.setWindowTitle('Anti-SPAM')
win.show()
win.move(650, 200)
sys.exit(app.exec_())
