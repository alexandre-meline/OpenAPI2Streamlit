def add_tabulation_to_multiline_string(multi_line_string: str) -> str:
    """
    Ajoute une tabulation au début de chaque ligne d'une chaîne multi-ligne.
    """
    # Diviser la chaîne multi-ligne en lignes individuelles
    lines = multi_line_string.split("\n")
    print(lines)
    
    # Ajouter une tabulation à chaque ligne
    tabulated_lines = [f"\t{line.strip()}" for line in lines]
    
    # Joindre les lignes tabulées en une seule chaîne
    tabulated_string = "\n".join(tabulated_lines)
    
    return tabulated_string


data = """"id": id,\n "account_type": account_type,\n "name": name,\n "initial_amout": initial_amout,\n "actualy_amout": actualy_amout,\n "user": user'"""

r = add_tabulation_to_multiline_string(data)
print(r)