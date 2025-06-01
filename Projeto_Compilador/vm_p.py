def get_var_index(ast):
    vars_section = next((v for (k, v) in ast if k == 'vars'), [])
    index = 0
    var_map = {}
    for var_list, tipo in vars_section:
        for var in var_list:
            if isinstance(tipo, tuple) and tipo[0] == 'array':
                _, start, end, _ = tipo
                start_idx = int(start)
                end_idx = int(end)
                var_map[var] = (index, start_idx)
                index += end_idx - start_idx + 1
            else:
                var_map[var] = index
                index += 1
    return var_map

def get_var_types(ast):
    vars_section = next((v for (k, v) in ast if k == 'vars'), [])
    var_types = {}
    for var_list, tipo in vars_section:
        for var in var_list:
            var_types[var] = tipo
    return var_types

def compile_expr(expr, var_map):
    code = []
    if isinstance(expr, tuple):
        if expr[0] == 'rel':
            op, left, right = expr[1], expr[2], expr[3]
            code += compile_expr(left, var_map)

            if isinstance(left, tuple) and left[0] == 'array' and isinstance(right, str) and len(right) == 1:
                code.append('PUSHI 49')
            else:
                code += compile_expr(right, var_map)

            if op == '<>':
                code.append('EQUAL')
                code.append('NOT')
            else:
                rel_ops = {
                    '>': 'SUP',
                    '>=': 'SUPEQ',
                    '<': 'INF',
                    '<=': 'INFEQ',
                    '=': 'EQUAL'
                }
                code.append(rel_ops[op])

        elif expr[0] == 'binop':
            op, left, right = expr[1], expr[2], expr[3]
            code += compile_expr(left, var_map)
            code += compile_expr(right, var_map)
            bin_ops = {
                '+': 'ADD',
                '-': 'SUB',
                '*': 'MUL',
                'div': 'DIV',
                'mod': 'MOD'
            }
            code.append(bin_ops[op])

        elif expr[0] == 'and':
            _, left, right = expr
            code += compile_expr(left, var_map)
            code += compile_expr(right, var_map)
            code.append('AND')

        elif expr[0] == 'or':
            _, left, right = expr
            code += compile_expr(left, var_map)
            code += compile_expr(right, var_map)
            code.append('OR')

        elif expr[0] == 'not':
            _, subexpr = expr
            code += compile_expr(subexpr, var_map)
            code.append('NOT')

        elif expr[0] == 'array':
            _, array_name, index_expr = expr
            if isinstance(var_map[array_name], tuple):
                base_index, logical_start = var_map[array_name]
                code.append('PUSHGP')
                code.append(f'PUSHI {base_index}')
                code.append('PADD')
                code += compile_expr(index_expr, var_map)
                code.append(f'PUSHI {logical_start}')
                code.append('SUB')
                code.append('LOADN')
            else:
                code.append(f'PUSHG {var_map[array_name]}')
                code += compile_expr(index_expr, var_map)
                code.append('PUSHI 1')
                code.append('SUB')
                code.append('CHARAT')

        elif expr[0] == 'func':
            func_name, args = expr[1]
            func_name = func_name.lower()
            if func_name == 'length':
                arg = args[0]
                code.append(f'PUSHG {var_map[arg]}')
                code.append('STRLEN')

        else:
            code.append(f'# Unsupported expr type: {expr}')

    elif isinstance(expr, str):
        if expr == 'true':
            code.append('PUSHI 1')
        elif expr == 'false':
            code.append('PUSHI 0')
        elif expr in var_map:
            code.append(f'PUSHG {var_map[expr]}')
        else:
            try:
                val = int(expr)
                code.append(f'PUSHI {val}')
            except ValueError:
                code.append(f'PUSHS "{expr}"')

    elif isinstance(expr, int):
        code.append(f'PUSHI {expr}')

    else:
        code.append(f'# Unsupported expr format: {expr}')

    return code

def compile_instr(instr, var_map, var_types, label_counter):
    code = []
    if instr[0] == 'func':
        func_name, args = instr[1]
        func_name = func_name.lower()

        if func_name == 'write':
            for arg in args:
                if arg in var_map:
                    code.append(f'PUSHG {var_map[arg]}')
                    code.append('WRITEI')
                else:
                    code.append(f'PUSHS "{arg}"')
                    code.append('WRITES')

        elif func_name == 'writeln':
            for arg in args:
                if arg in var_map:
                    code.append(f'PUSHG {var_map[arg]}')
                    code.append('WRITEI')
                else:
                    code.append(f'PUSHS "{arg}"')
                    code.append('WRITES')
            code.append('WRITELN')

        elif func_name == 'readln':
            var = args[0]
            if isinstance(var, tuple) and var[0] == 'array':
                _, array_name, index_expr = var
                base_index, logical_start = var_map[array_name]
                code.append('PUSHGP')
                code.append(f'PUSHI {base_index}')
                code.append('PADD')
                code += compile_expr(index_expr, var_map)
                code.append(f'PUSHI {logical_start}')
                code.append('SUB')
                code.append('READ')
                code.append('ATOI')
                code.append('STOREN')
            else:
                tipo = var_types.get(var, None)
                if tipo == 'string':
                    code.append('READ')
                    code.append(f'STOREG {var_map[var]}')
                else:
                    code.append('READ')
                    code.append('ATOI')
                    code.append(f'STOREG {var_map[var]}')
        else:
            code.append(f'# Unsupported function: {func_name}')

    elif instr[0] == 'atrib':
        _, var, expr = instr
        code += compile_expr(expr, var_map)
        code.append(f'STOREG {var_map[var]}')

    elif instr[0] == 'if':
        cond = next(x[1] for x in instr[1] if x[0] == 'cond')
        then_block = next(x[1] for x in instr[1] if x[0] == 'then')

        label_end = f'label{label_counter[0]}'
        label_counter[0] += 1

        code += compile_expr(cond, var_map)
        code.append(f'JZ {label_end}')

        for i in (then_block if isinstance(then_block, list) else [then_block]):
            code += compile_instr(i, var_map, var_types, label_counter)

        code.append(f'{label_end}:')

    elif instr[0] == 'if_else':
        cond = next(x[1] for x in instr[1] if x[0] == 'cond')
        then_block = next(x[1] for x in instr[1] if x[0] == 'then')
        else_block = next(x[1] for x in instr[1] if x[0] == 'else')

        label_else = f'label{label_counter[0]}'
        label_end = f'label{label_counter[0] + 1}'
        label_counter[0] += 2

        code += compile_expr(cond, var_map)
        code.append(f'JZ {label_else}')

        for i in (then_block if isinstance(then_block, list) else [then_block]):
            code += compile_instr(i, var_map, var_types, label_counter)
        code.append(f'JUMP {label_end}')

        code.append(f'{label_else}:')
        for i in (else_block if isinstance(else_block, list) else [else_block]):
            code += compile_instr(i, var_map, var_types, label_counter)
        code.append(f'{label_end}:')

    elif instr[0] == 'for':
        inicio = next(x[1] for x in instr[1] if x[0] == 'inicio')
        fim = next(x[1] for x in instr[1] if x[0] == 'fim')
        conteudo = next(x[1] for x in instr[1] if x[0] == 'conteudo')

        label_start = f'label{label_counter[0]}'
        label_end = f'label{label_counter[0] + 1}'
        label_counter[0] += 2

        code += compile_instr(inicio, var_map, var_types, label_counter)
        code.append(f'{label_start}:')

        code.append(f'PUSHG {var_map[inicio[1]]}')
        code += compile_expr(fim, var_map)
        code.append('INFEQ')
        code.append(f'JZ {label_end}')

        if isinstance(conteudo, list):
            for instr_interno in conteudo:
                code += compile_instr(instr_interno, var_map, var_types, label_counter)
        else:
            code += compile_instr(conteudo, var_map, var_types, label_counter)

        code.append(f'PUSHG {var_map[inicio[1]]}')
        code.append('PUSHI 1')
        code.append('ADD')
        code.append(f'STOREG {var_map[inicio[1]]}')

        code.append(f'JUMP {label_start}')
        code.append(f'{label_end}:')

    elif instr[0] == 'for_downto':
        inicio = next(x[1] for x in instr[1] if x[0] == 'inicio')
        fim = next(x[1] for x in instr[1] if x[0] == 'fim')
        conteudo = next(x[1] for x in instr[1] if x[0] == 'conteudo')

        label_start = f'label{label_counter[0]}'
        label_end = f'label{label_counter[0] + 1}'
        label_counter[0] += 2

        code += compile_instr(inicio, var_map, var_types, label_counter)
        code.append(f'{label_start}:')

        code.append(f'PUSHG {var_map[inicio[1]]}')
        code += compile_expr(fim, var_map)
        code.append('SUPEQ')
        code.append(f'JZ {label_end}')

        if isinstance(conteudo, list):
            for instr_interno in conteudo:
                code += compile_instr(instr_interno, var_map, var_types, label_counter)
        else:
            code += compile_instr(conteudo, var_map, var_types, label_counter)

        code.append(f'PUSHG {var_map[inicio[1]]}')
        code.append('PUSHI 1')
        code.append('SUB')
        code.append(f'STOREG {var_map[inicio[1]]}')

        code.append(f'JUMP {label_start}')
        code.append(f'{label_end}:')

    elif instr[0] == 'while':
        cond = next(x[1] for x in instr[1] if x[0] == 'cond')
        conteudo = next(x[1] for x in instr[1] if x[0] == 'conteudo')

        label_start = f'label{label_counter[0]}'
        label_end = f'label{label_counter[0] + 1}'
        label_counter[0] += 2

        code.append(f'{label_start}:')
        code += compile_expr(cond, var_map)
        code.append(f'JZ {label_end}')

        if isinstance(conteudo, list):
            for instr_interno in conteudo:
                code += compile_instr(instr_interno, var_map, var_types, label_counter)
        else:
            code += compile_instr(conteudo, var_map, var_types, label_counter)

        code.append(f'JUMP {label_start}')
        code.append(f'{label_end}:')

    else:
        code.append(f'# Unsupported instruction: {instr}')

    return code

def compile_to_maq(ast):
    maq_code = []
    var_map = get_var_index(ast)
    var_types = get_var_types(ast)
    label_counter = [0]

    for _ in range(len(var_map)):
        maq_code.append('PUSHI 0')
    for i in range(len(var_map)):
        maq_code.append(f'STOREG {i}')

    corpo = next((v for (k, v) in ast if k == 'corpo'), [])
    for instr in corpo:
        maq_code += compile_instr(instr, var_map, var_types, label_counter)

    maq_code.append('STOP')
    return maq_code

# -------- EXEMPLO DE USO ----------

if __name__ == '__main__':
    programa = [('nome_programa', 'SomaArray'),
 ('functions', []),
 ('vars',
  [(['numeros'], ('array', '1', '5', 'integer')), (['i', 'soma'], 'integer')]),
 ('corpo',
  [('atrib', 'soma', '0'),
   ('func', ('writeln', ['Introduza 5 nmeros inteiros:'])),
   ('for',
    [('inicio', ('atrib', 'i', '1')),
     ('fim', '5'),
     ('conteudo',
      [('func', ('readln', [('array', 'numeros', 'i')])),
       ('atrib', 'soma', ('binop', '+', 'soma', ('array', 'numeros', 'i')))])]),
   ('func', ('writeln', ['A soma dos nmeros : ', 'soma']))])]

    codigo = compile_to_maq(programa)
    print('\n'.join(codigo))
