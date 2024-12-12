import ply.lex as lex
import ply.yacc as yacc

# Définition des tokens
tokens = [
    'STARTUML', 'ENDUML', 'ACTOR', 'USECASE', 'PACKAGE',
    'AS', 'ID', 'STRING', 'LBRACE', 'RBRACE'
]

# Expressions régulières pour les tokens
t_STARTUML = r'@startuml'
t_ENDUML = r'@enduml'

t_USECASE = r'usecase'
t_PACKAGE = r'package'
t_AS = r'as'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_STRING = r'"[^"]*"'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

# Ignorer les espaces et tabulations
t_ignore = ' \t'

# Gestion des erreurs lexicales
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractère illégal '{t.value[0]}' à la ligne {t.lineno}")
    t.lexer.skip(1)

# Construire l'analyseur lexical
lexer = lex.lex()

# Règles de grammaire
def p_start(p):
    '''start : STARTUML content ENDUML'''
    p[0] = ('diagram', p[2])

def p_content(p):
    '''content : content line
               | line'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_line(p):
    '''line : actor_def
            | usecase_def
            | package_def'''
    p[0] = p[1]

# Règle pour un acteur défini en dehors d'un paquet
def p_actor_def(p):
    '''actor_def : ACTOR ID'''
    p[0] = ('actor', p[2])

# Règle pour un acteur à l'intérieur d'un paquet
def p_actor_in_package_def(p):
    '''actor_in_package_def : PACKAGE ID LBRACE content RBRACE actor_def'''
    p[0] = ('actor_in_package', p[2], p[6])

def p_usecase_def(p):
    '''usecase_def : USECASE STRING AS ID'''
    p[0] = ('usecase', p[2], p[4])

def p_package_def(p):
    '''package_def : PACKAGE ID LBRACE content RBRACE'''
    p[0] = ('package', p[2], p[4])

# Gestion des erreurs syntaxiques
def p_error(p):
    if p:
        print(f"Erreur de syntaxe au token '{p.value}', ligne {p.lineno}")
    else:
        print("Erreur de syntaxe à la fin du fichier")

# Construire le parser
parser = yacc.yacc()

# Exemple de diagramme UML corrigé
example = """
@startuml
actor User
usecase "Login"
package Main {
    actor Admin
    usecase "Manage System"
}
@enduml
"""

# Analyse lexicale
print("Analyse lexicale :")
lexer.input(example)
for tok in lexer:
    print(tok)

# Analyse syntaxique
print("\nAnalyse syntaxique :")
result = parser.parse(example)
print(result)
