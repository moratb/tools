def cumsum_is_paid(x, mode):
    """Функция помечает строки. 1 - платная, 0 - бесплатная"""
    cur = 0
    res = []
    hard_acum = []
    for v in x:
        if cur == 0:
            is_paid = 0
        else:
            is_paid = 1
        cur += v
        
        if cur < 0:
            cur = 0
            
        hard_acum.append(cur)
        res += [is_paid]    
        
    if mode == 'mark':
        return res
    elif mode == 'value':
        return hard_acum
