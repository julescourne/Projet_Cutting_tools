def get_distance(p, q, coef_tab):
    """
    Retourne la distance entre deux points p et q qui ont le meme nombre de dimension

    On assume que coeff_tab est la longeur de p et q
    si pas de pondération : coef_tab = [1 in range(0,len(q))]
    """
    sum_sq_difference = 0
    for p_i, q_i, coeff_i in zip(p, q, coef_tab):
        sum_sq_difference += coeff_i * ((p_i - q_i) ** 2)

    distance = sum_sq_difference ** 0.5
    return distance