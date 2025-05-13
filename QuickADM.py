import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk  # Necessário para usar tk.Text

from tkinter.simpledialog import askstring
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile
import os
import random
import json
import os
from tkcalendar import DateEntry

class Registro:
    def __init__(self, nome, data, hora, nivel, motivo): 
        self.nome = nome
        self.data = data
        self.hora = hora
        self.nivel = nivel
        self.motivo = motivo
        

    def to_tuple(self):
        return (self.nome, self.data, self.hora, self.nivel, self.motivo)

def mostrar_splash():
    splash = tb.Toplevel()
    splash.overrideredirect(True)  
    splash.configure(bg="#FFFFFF") 

    largura, altura = 400, 200 
    largura_tela = splash.winfo_screenwidth()
    altura_tela = splash.winfo_screenheight()
    pos_x = (largura_tela - largura) // 2
    pos_y = (altura_tela - altura) // 2
    splash.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

   
    frame_borda = tb.Frame(splash, bootstyle="dark", padx=2, pady=2)
    frame_borda.pack(expand=True, fill="both")


   
    conteudo = tb.Frame(frame_borda, bootstyle="light")
    conteudo.pack(expand=True, fill="both")

    logo_path = "logo.png"  
    try:
        from PIL import Image, ImageTk
        imagem = Image.open(logo_path).resize((300, 300))
        logo = ImageTk.PhotoImage(imagem)
        label = tb.Label(conteudo, image=logo,bootstyle="light")
        label.image = logo  
        label.pack(expand=True)
    except:
        tb.Label(conteudo, text="Logo não encontrada",bootstyle="light").pack(expand=True)

    splash.after(3000, splash.destroy)  
    return splash


class Registro:
    def __init__(self, nome, data, hora, nivel, motivo):
        self.nome = nome
        self.data = data
        self.hora = hora
        self.nivel = nivel
        self.motivo = motivo

    def to_tuple(self):
        return (self.nome, self.data, self.hora, self.nivel, self.motivo)

    def to_dict(self):
        return {
            "nome": self.nome,
            "data": self.data,
            "hora": self.hora,
            "nivel": self.nivel,
            "motivo": self.motivo
        }

class App(tb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("🌻 QuickADM - Saída antecipada")
        self.state("zoomed")
        largura_janela = 900
        altura_janela = 500

        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        pos_x = (largura_tela - largura_janela) // 2
        pos_y = (altura_tela - altura_janela) // 2

        self.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        self.resizable(False, False)
        self.registros = []

        self.notebook = tb.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        self.registrar_frame = tb.Frame(self.notebook, padding=10)
        self.consultar_frame = tb.Frame(self.notebook, padding=10)
        self.imprimir_frame = tb.Frame(self.notebook, padding=10)
        self.opcoes_frame = tb.Frame(self.notebook, padding=10)  # Alterado para Opções

        self.notebook.add(self.registrar_frame, text="Registrar Saída")
        self.notebook.add(self.consultar_frame, text="Consultar Saídas")
        self.notebook.add(self.imprimir_frame, text="Imprimir Saídas")
        self.notebook.add(self.opcoes_frame, text="Opções")  # Alterado para Opções

        self.criar_tela_registro()
        self.criar_tela_consulta()
        self.criar_tela_impressao()
        self.criar_tela_opcoes()  # Nova função para Opções
        self.carregar_registros()

    def criar_tela_opcoes(self):
        f = self.opcoes_frame

        # Botão para Modo Desenvolvedor
        tb.Button(f, text="🔧 Modo Desenvolvedor", command=self.verificar_acesso_dev, width=40).pack(pady=5)

        # Botão para Novidades
        tb.Button(f, text="📜 Novidades", command=self.mostrar_novidades, width=40).pack(pady=5)

        # Botão para Sair
        tb.Button(f, text="❌ Sair", command=self.sair, width=40).pack(pady=5)

    def mostrar_novidades(self):
        att = (
            "Novidades da versão 1.2.0:\n\n"
            "Adicionada a aba \"Opções\", que substitui a aba \"Novidades\".\n\n"
            "Adicionada a opção de sair da aplicação diretamente na aba Opções.\n\n"
            "Adicionado o botão \"Modo Desenvolvedor\", para permitir o acesso ao modo para testes.\n\n"
            "Inserida marca d’água na primeira página ao imprimir o relatório de saídas.\n\n"
            "Melhorado a tela de editar registros."
        )

        # Nova janela para mostrar as novidades
        novidades_win = tb.Toplevel(self)
        novidades_win.title("Novidades")
        novidades_win.geometry("400x300")
        novidades_win.resizable(False, False)

        tb.Label(novidades_win, text=att, font=("Helvetica", 10), justify="left", wraplength=350).pack(pady=20)

    def sair(self):
        # Fecha o aplicativo
        self.quit()


    def criar_tela_registro(self):
        f = self.registrar_frame

        # Frame interno para centralizar
        conteudo = tb.Frame(f)
        conteudo.place(relx=0.5, rely=0.3, anchor="n")  # Centraliza horizontalmente, ajusta vertical como quiser

        # Configura grid do frame interno
        for i in range(4):
            conteudo.columnconfigure(i, weight=1)

        tb.Label(conteudo, text="Nome do Aluno:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.nome_entry = tb.Entry(conteudo, width=40)
        self.nome_entry.grid(row=0, column=1, columnspan=3, sticky="ew", padx=10, pady=5)

        tb.Label(conteudo, text="Data (DD/MM/AAAA):").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.data_entry = DateEntry(conteudo, date_pattern='dd/MM/yyyy', locale='pt_BR')
        self.data_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        tb.Label(conteudo, text="Horário (HH:MM):").grid(row=1, column=2, sticky="e", padx=10, pady=5)
        self.hora_entry = tb.Entry(conteudo)
        self.hora_entry.grid(row=1, column=3, sticky="ew", padx=10, pady=5)

        tb.Label(conteudo, text="Nível:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.nivel_cb = tb.Combobox(conteudo, values=["BA", "BB", "1A", "1B", "1C", "2A", "2B", "2C", "PRÉ"], state="readonly")
        self.nivel_cb.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        self.nivel_cb.set("Escolha")

        tb.Label(conteudo, text="Motivo da Saída:").grid(row=3, column=0, sticky="ne", padx=10, pady=5)
        self.motivo_text = tb.Text(conteudo, height=4, width=60)
        self.motivo_text.grid(row=3, column=1, columnspan=3, sticky="nsew", padx=10, pady=5)

        tb.Button(conteudo, text="Registrar", command=self.registrar_saida).grid(row=4, column=1, columnspan=2, sticky="ew", padx=10, pady=10)



    
    def verificar_acesso_dev(self):
        senha = askstring("Modo desenvolvedor", "CHAVE DE ACESSO:", show="*")
        if senha == "dev1406":
            if hasattr(self, 'btn_gerar_testes'):
                self.btn_gerar_testes.pack(side="left", padx=5)
            messagebox.showinfo("Acesso Concedido", "MODO DESENVOLVEDOR ATIVADO")
        else:
            messagebox.showerror("Acesso Negado", "Senha incorreta.")

    def salvar_registros(self):
        dados = [r.to_dict() for r in self.registros]
        with open("registros.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
    
    def carregar_registros(self):
        if os.path.exists("registros.json"):
            with open("registros.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.registros = [Registro(**d) for d in dados]
        self.atualizar_tabela()

    def registrar_saida(self):
        nome = self.nome_entry.get().strip()
        data = self.data_entry.get().strip()
        hora = self.hora_entry.get().strip()
        nivel = self.nivel_cb.get()
        motivo = self.motivo_text.get("1.0", tk.END).strip()

        if not all([nome, data, hora, motivo]):
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return
    
        if nivel == "Escolha":
            messagebox.showwarning("Campos obrigatórios", "Escolha um nível.")
            return

        try:
            datetime.strptime(data, "%d/%m/%Y")
            datetime.strptime(hora, "%H:%M")
        except ValueError:
            messagebox.showerror("Formato inválido", "Use o formato correto de data e hora.")
            return

        reg = Registro(nome, data, hora, nivel, motivo)
        self.registros.append(reg)
        self.salvar_registros()

        self.nome_entry.delete(0, tk.END)
        self.data_entry.delete(0, tk.END)
        self.hora_entry.delete(0, tk.END)
        self.motivo_text.delete("1.0", tk.END)
        messagebox.showinfo("Registrado", "Saída registrada com sucesso.")
        self.atualizar_tabela()

    def criar_tela_consulta(self):
        f = self.consultar_frame

        # Filtros
        filtro_frame = tb.Frame(f)
        filtro_frame.pack(fill="x", pady=5)

        tb.Label(filtro_frame, text="Filtrar por Nome:").grid(row=0, column=0, padx=5)
        self.filtro_nome = tb.Entry(filtro_frame, width=20)
        self.filtro_nome.grid(row=0, column=1)

        tb.Label(filtro_frame, text="Data:").grid(row=0, column=2, padx=5)
        self.filtro_data = tb.Entry(filtro_frame, width=12)
        self.filtro_data.grid(row=0, column=3)

        tb.Label(filtro_frame, text="Nível:").grid(row=0, column=4, padx=5)
        self.filtro_nivel = tb.Combobox(filtro_frame, values=["Todos", "BA", "BB", "1A", "1B", "1C", "2A", "2B", "2C", "PRÉ"], state="readonly", width=12)
        self.filtro_nivel.grid(row=0, column=5)
        self.filtro_nivel.set("Todos")

        tb.Button(filtro_frame, text="Filtrar", command=self.atualizar_tabela).grid(row=0, column=6, padx=10)

        # Tabela
        self.tree = ttk.Treeview(f, columns=("Nome", "Data", "Hora", "Nível", "Motivo"), show="headings", height=15)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130 if col != "Motivo" else 200)
        self.tree.pack(fill="both", expand=True)

        # Botões
        btn_frame = tb.Frame(f)
        btn_frame.pack(pady=5)

        tb.Button(btn_frame, text="Editar Selecionado", command=self.editar_registro).pack(side="left", padx=5)
        tb.Button(btn_frame, text="Excluir Selecionado", command=self.excluir_registro).pack(side="left", padx=5)

        self.btn_gerar_testes = tb.Button(btn_frame, text="Gerar Registros de Teste", command=self.preencher_registros_teste)
        self.btn_gerar_testes.pack(side="left", padx=5)
        self.btn_gerar_testes.pack_forget()


    
    def criar_tela_novidades(self):
        f = self.novidades_frame
        att = (
            "Novidades da versão 1.2.0:\n\n"
            "Adicionada a aba \"Opções\"\n\n"
            "Adicionado o \"Modo Desenvolvedor\" para testes do programa"
            "Ao acionar o modo desenvolvedor, cria-se o botão \"Gerar registros\", que cria automaticamente 30 registros para testes de desenvolvimento.\n\n"
            "Inserida marca d’água na primeira página ao imprimir o relatório de saídas.\n\n"
            "Adicionado sistema de salvamento em json.\n\n"
            "Melhorado a tela de editar registros.\n\n"
            "Adicionado DatePicker e Automatização de data.\n\n"
            "Reajustado o tamanho da janela.\n\n"
            "Erros corrigidos e melhorias no programa."

        )

        tb.Button(f, text="🔧 Acesso DEV", command=self.verificar_acesso_dev).pack(pady=10)


        tb.Label(f, text=att, font=("Helvetica", 10), justify="left", wraplength=600).pack(pady=20)



    def atualizar_tabela(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        nome_f = self.filtro_nome.get().strip().lower()
        data_f = self.filtro_data.get().strip()
        nivel_f = self.filtro_nivel.get()

        for r in self.registros:
            if nome_f and nome_f not in r.nome.lower():
                continue
            if data_f and data_f != r.data:
                continue
            if nivel_f != "Todos" and nivel_f != r.nivel:
                continue
            self.tree.insert("", "end", values=r.to_tuple())
    
    def preencher_registros_teste(self):
        nomes = ["Ana", "Bruno", "Carlos", "Daniela", "Eduarda", "Felipe", "Gabriela", "Henrique", "Isabela", "João"]
        niveis = ["BA", "BB", "1A", "1B", "1C", "2A", "2B", "2C", "PRÉ"]
        motivos = ["Consulta médica", "Emergência familiar", "Dor de cabeça", "Dentista", "Viagem", "Consulta oftalmo", "Febre", "Reunião com pais"]

        for _ in range(30):
            nome = random.choice(nomes)
            data = datetime.now().strftime("%d/%m/%Y")
            hora = f"{random.randint(7, 15):02d}:{random.randint(0,59):02d}"
            nivel = random.choice(niveis)
            motivo = random.choice(motivos)
            self.registros.append(Registro(nome, data, hora, nivel, motivo))

        self.atualizar_tabela()
        messagebox.showinfo("Registros de Teste", "30 registros de teste foram adicionados com sucesso.")

    def editar_registro(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selecionar", "Selecione um registro para editar.")
            return

        item = self.tree.item(selected[0])["values"]
        nome, data, hora, nivel, motivo = item

        # Nova janela
        edit_win = tb.Toplevel(self)
        edit_win.title("Editar Registro")
        edit_win.geometry("400x400")
        edit_win.resizable(False, False)

        # Nome
        tb.Label(edit_win, text="Nome:").pack(pady=5)
        nome_entry = tb.Entry(edit_win, width=40)
        nome_entry.pack()
        nome_entry.insert(0, nome)

        # Data
        tb.Label(edit_win, text="Data (DD/MM/AAAA):").pack(pady=5)
        data_entry = DateEntry(edit_win, date_pattern='dd/MM/yyyy', locale='pt_BR')
        data_entry.pack()
        data_entry.set_date(datetime.strptime(data, "%d/%m/%Y"))

        # Hora
        tb.Label(edit_win, text="Hora (HH:MM):").pack(pady=5)
        hora_entry = tb.Entry(edit_win, width=20)
        hora_entry.pack()
        hora_entry.insert(0, hora)

        # Nível
        tb.Label(edit_win, text="Nível:").pack(pady=5)
        nivel_cb = tb.Combobox(edit_win, values=["BA", "BB", "1A", "1B", "1C", "2A", "2B", "2C", "PRÉ"], state="readonly")
        nivel_cb.pack()
        nivel_cb.set(nivel)

        # Motivo
        tb.Label(edit_win, text="Motivo da Saída:").pack(pady=5)
        motivo_text = tb.Text(edit_win, height=5, width=40)
        motivo_text.pack()
        motivo_text.insert("1.0", motivo)

        def salvar_edicao():
            novo_nome = nome_entry.get().strip()
            nova_data = data_entry.get().strip()
            nova_hora = hora_entry.get().strip()
            novo_nivel = nivel_cb.get()
            novo_motivo = motivo_text.get("1.0", tk.END).strip()

            # Atualiza no banco de registros
            for r in self.registros:
                if r.to_tuple() == tuple(item):
                    r.nome = novo_nome
                    r.data = nova_data
                    r.hora = nova_hora
                    r.nivel = novo_nivel
                    r.motivo = novo_motivo
                    break

            self.atualizar_tabela()
            edit_win.destroy()
            messagebox.showinfo("Atualizado", "Registro editado com sucesso.")

        tb.Button(edit_win, text="Salvar Alterações", command=salvar_edicao).pack(pady=15)



    def excluir_registro(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selecionar", "Selecione um registro para excluir.")
            return

        item = self.tree.item(selected[0])["values"]

        confirm = messagebox.askyesno("Confirmar", "Deseja realmente excluir este registro?")
        if not confirm:
            return

        for r in self.registros:
            if r.to_tuple() == tuple(item):
                self.registros.remove(r)
                break

        self.salvar_registros()
        self.atualizar_tabela()
        messagebox.showinfo("Excluído", "Registro excluído com sucesso.")

    def criar_tela_impressao(self):
        f = self.imprimir_frame

        filtro_frame = tb.Frame(f)
        filtro_frame.pack(pady=10)

        tb.Label(filtro_frame, text="Filtrar por Nome:").grid(row=0, column=0, padx=5)
        self.print_nome = tb.Entry(filtro_frame, width=20)
        self.print_nome.grid(row=0, column=1)

        tb.Label(filtro_frame, text="Data:").grid(row=0, column=2, padx=5)
        self.print_data = tb.Entry(filtro_frame, width=12)
        self.print_data.grid(row=0, column=3)

        tb.Label(filtro_frame, text="Nível:").grid(row=0, column=4, padx=5)

        self.print_nivel = tb.Combobox(filtro_frame, values=["Todos", "BA", "BB", "1A", "1B", "1C", "2A", "2B", "2C", "PRÉ"], state="readonly", width=12)

        self.print_nivel.grid(row=0, column=5)
        self.print_nivel.set("Todos")

        tb.Button(filtro_frame, text="Gerar PDF", command=self.gerar_pdf).grid(row=0, column=6, padx=10)

    def gerar_pdf(self):
        nome_f = self.print_nome.get().strip().lower()
        data_f = self.print_data.get().strip()
        nivel_f = self.print_nivel.get()

        filtradas = []
        for r in self.registros:
            if nome_f and nome_f not in r.nome.lower():
                continue
            if data_f and data_f != r.data:
                continue
            if nivel_f != "Todos" and nivel_f != r.nivel:
                continue
            filtradas.append(r)

        if not filtradas:
            messagebox.showinfo("Nada a imprimir", "Nenhum registro corresponde aos filtros.")
            return

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        c = canvas.Canvas(temp_file.name, pagesize=A4)
        width, height = A4
        y = height - 40
        marca = "https://institutocasagirassol.com.br/wp-content/uploads/2021/08/logo_Prancheta_1.png"  
        c.saveState()
        c.translate(width / 2, height / 2)
        c.rotate(45)  
        c.setFillAlpha(0.2) 
        c.drawImage(marca, -200, -200, width=400, height=400, preserveAspectRatio=True, mask='auto')
        c.restoreState()

        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, y, "Relatório de Saídas de Alunos - CMEI Lucineia")
        y -= 30
        c.setFont("Helvetica", 10)

        for r in filtradas:
            texto = f"{r.data} {r.hora} | {r.nome} | {r.nivel} | {r.motivo}"
            c.drawString(40, y, texto)
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 40
        c.save()
        os.startfile(temp_file.name)

if __name__ == "__main__":
    splash = mostrar_splash()
    splash.after(3000, lambda: (splash.destroy(), App().mainloop()))