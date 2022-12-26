from os import path
from random import randint
from sys import argv
from time import sleep
from webbrowser import open_new

from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtWidgets import *


def initwindow():
    def iniciar():
        load = 0
        while load < 100:
            janela.showMessage(f"Carregando Modulos: {load}%", align, Qt.GlobalColor.black)
            sleep(0.5)
            load += randint(2, 10)
        janela.close()
        app.ferramentas.show()

    img = QPixmap(path.abspath("favicon/favicon-512x512.png"))
    align = int(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignAbsolute)
    janela = QSplashScreen(img)
    janela.setStyleSheet(tema)
    janela.show()
    iniciar()


class GCR:
    def __init__(self):
        # criando a instancia principal do programa
        self.gc = QApplication(argv)

        QFontDatabase.addApplicationFont(path.abspath("font/copse.ttf"))

        # criando a instancia de leitura do ficheiro pdf
        self.pdfile = QPdfDocument(self.gc)

        # criando a instancia da janela do programa e seu tamanho
        self.ferramentas = QMainWindow()
        self.ferramentas.setMinimumSize(900, 500)
        self.ferramentas.setWindowIcon(QIcon(path.abspath("favicon/favicon-192x192.png")))
        self.ferramentas.setWindowTitle("gcreader - PDF reader")
        self.ferramentas.setStyleSheet(tema)

        # barra de menu
        menu_ferramentas = QMenuBar()
        opcoes = menu_ferramentas.addMenu("Opções")

        abrir = opcoes.addAction("Abrir")
        abrir.triggered.connect(self.pdfopen)
        opcoes.addSeparator()

        instr = opcoes.addAction("Instruções")
        instr.triggered.connect(self._instr)
        opcoes.addSeparator()

        _sair = lambda: self.gc.exit(0)
        sair = opcoes.addAction("Sair")
        sair.triggered.connect(_sair)

        sobre = menu_ferramentas.addAction("Sobre")
        sobre.triggered.connect(self._sobre)
        self.ferramentas.setMenuBar(menu_ferramentas)

        # ferramnta central da janela
        centralwidget = QWidget()
        centrallayout = QVBoxLayout()

        self.tabset = QTabWidget()
        self.tabset.setTabBarAutoHide(True)
        self.tabset.setDocumentMode(True)
        self.tabset.setTabsClosable(True)
        self.tabset.tabCloseRequested.connect(self.fechar)
        centrallayout.addWidget(self.tabset)

        def browser():
            open_new('https://artesgc.home.blog')

        labelcopyright = QLabel("<a href='#' style='text-decoration:none;'>&trade;ArtesGC Inc.</a>", self.ferramentas)
        labelcopyright.setAlignment(Qt.AlignmentFlag.AlignCenter)
        labelcopyright.setToolTip('Acesso a pagina oficial da ArtesGC!')
        labelcopyright.setStyleSheet(
            "background-color: gray;"
            "border-radius: 5px;"
            "padding: 5px;"
        )
        labelcopyright.linkActivated.connect(browser)
        centrallayout.addWidget(labelcopyright)
        centralwidget.setLayout(centrallayout)

        self.ferramentas.setCentralWidget(centralwidget)

        # chamando a janela do programa
        self.janelainicial()

    def janelainicial(self):
        frame = QFrame()
        layout = QVBoxLayout()

        labelintro = QLabel(
            """
            <h1>Bem Vindo ao GCreader</h1><hr>
            <p>Um simples e pratico<br>leitor de ficheiros PDF</p><br>
            <p><a href="#">Clique para abrir algum ficheiro..</a></p>
            """
        )
        labelintro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        labelintro.linkActivated.connect(self.pdfopen)
        layout.addWidget(labelintro)
        frame.setLayout(layout)
        self.tabset.addTab(frame, "Pagina Inicial")

    def _sobre(self):
        QMessageBox.information(self.ferramentas,  "Sobre",
                                "<b>Informações sobre o Programa</b><hr>"
                                "<p><ul><li><b>Nome:</b> GCreader</li>"
                                "<li><b>Versão:</b> 0.2-122022</li>"
                                "<li><b>Programador:</b> &copy;Nurul-GC</li>"
                                "<li><b>Empresa:</b> &trade;ArtesGC, Inc.</li></ul></p>")

    def _instr(self):
        QMessageBox.information(self.ferramentas, "Instruções",
                                "<b>Breve Apresentação</b><hr>"
                                "<p>GCreader é um simples leitor de PDFs, prático, leve e eficiente!<br>"
                                "É possivel abri-lo directamente apartir de um ficheiro PDF no explorador ou chama-lo "
                                "pelo executavel no menu iniciar ou ainda localizar o icone no ambiente de "
                                "trabalho.</p> "
                                "<p>Obrigado pelo seu suporte!<br>"
                                "<b>&trade;ArtesGC, Inc.</b></p>")

    def pdfviewer(self, pdfile: str):
        """janela de visualizacao dos ficheiros"""
        frame = QFrame()
        layout = QVBoxLayout()

        self.pdfile.load(pdfile)
        pdfviewer = QPdfView(self.ferramentas)
        pdfviewer.setDocument(self.pdfile)
        pdfviewer.setPageMode(pdfviewer.PageMode.MultiPage)
        layout.addWidget(pdfviewer)

        fchrbtn = QPushButton("Fechar")
        fchrbtn.clicked.connect(self.fechar)
        layout.addWidget(fchrbtn)

        frame.setLayout(layout)
        self.tabset.addTab(frame, path.split(pdfile)[-1])
        self.tabset.setCurrentWidget(frame)

    def pdfopen(self):
        pdfilename = QFileDialog.getOpenFileName(
                self.ferramentas,
                caption="Choose the PDF file",
                filter="PDF Files (*.pdf)"
        )[0]
        if pdfilename.isspace() or pdfilename == "":
            QMessageBox.warning(self.ferramentas, "Falha ao carregar ficheiro",
                                "Lamento, ficheiro não encontrado ou processo de procura cancelado!")
        else:
            self.pdfviewer(pdfilename)

    def fechar(self):
        if self.tabset.currentIndex() == 0:
            pass
        else:
            self.tabset.removeTab(self.tabset.currentIndex())


if __name__ == '__main__':
    tema = open(path.abspath("theme/gcr.qss")).read().strip()
    app = GCR()

    if len(argv) >= 2:
        app.pdfviewer(argv[1])
        initwindow()
        app.gc.exec()
    else:
        initwindow()
        app.gc.exec()
