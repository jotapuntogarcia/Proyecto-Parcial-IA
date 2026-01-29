import os

personajes = [
    {
        "Nombre": "Alan Turing",
        "Nacimiento": "23-06-12",
        "Aportes": "test de turing, la maquina bombe" #Se comio una manzana :?"
    },
    {
        "Nombre": "John",
        "Nacimiento": "4-9-27",
        "Aportes": "Creador del termino IA, creacion lenguaje LISP"
    },
    {
        "Nombre": "Minsky",
        "Nacimiento": "9-8-27",
        "Aportes": "Redes neuronales, analisis de perceptrones"
    },
    {
        "Nombre": "McCulloh",
        "Nacimiento": "16-11-1946",
        "Aportes": "Primer modelo de neuronas artificiales, vinculacion logoico booleano a neurofisica"
    },
    {
        "Nombre": "Pitts",
        "Nacimiento": "20-04-43",
        "Aportes": "Redes neuronales con McCulloh, teoria automata de finitos"
    },
    {
        "Nombre": "Hebb",
        "Nacimiento": "22-06-04",
        "Aportes": "Ley de Hebb, asamblea celular"
    },
    {
        "Nombre": "Samuel",
        "Nacimiento": "5-12-1901",
        "Aportes": "Aprendizaje automatico, machine learning"
    }
]# type: ignore

#si borro eso de arriba aparece error

markdown_table = "Nombre                Nacimiento             Aportes \n"

markdown_table += "-------------------  -----------      ------------------ \n"

for personaje in personajes:
    markdown_table += (
        f"{personaje['Nombre']:<18} "
        f"{personaje['Nacimiento']:<20} "
        f"{personaje['Aportes']:<55}\n"
    )
    
    print(markdown_table)
    
    file_path = "table_personajes.md"
    with open(file_path, "w", encoding="utf-8") as archivo:
        archivo.write(markdown_table)
        
    print(f"La tabla se ha guardado en el archivo: {file_path}")    