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

def get_function_info(ast):
    """Extrae información de las funciones definidas en el AST"""
    functions_section = next((v for (k, v) in ast if k == 'functions'), [])
    functions = {}
    
    if not functions_section:
        return functions
    
    # Procesar cada función
    func_data = {}
    for item in functions_section:
        if isinstance(item, tuple):
            key, value = item
            func_data[key] = value
    
    if 'nome_function' in func_data:
        func_name = func_data['nome_function']
        functions[func_name] = {
            'args': func_data.get('argsFunction', []),
            'return_type': func_data.get('tipoFunction', 'void'),
            'vars': func_data.get('varsFunction', []),
            'body': func_data.get('corpoFunction', [])
        }
    
    return functions

def get_function_var_map(func_info, func_name):
    """Crea un mapa de variables para una función específica"""
    var_map = {}
    index = 0
    
    # Primero los argumentos (están en posiciones negativas desde fp)
    arg_count = 0
    for arg_list, tipo in func_info['args']:
        for arg in arg_list:
            var_map[arg] = -(arg_count + 3)  # -3, -4, -5, ... (considerando fp[-1]=pc, fp[-2]=fp_anterior)
            arg_count += 1
    
    # Variables locales (posiciones positivas desde fp)
    for var_list, tipo in func_info['vars']:
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
    
    # Variable especial para el valor de retorno (mismo nombre que la función)
    if func_name not in var_map:
        var_map[func_name] = index
        index += 1
    
    return var_map, index

def get_function_var_types(func_info):
    """Obtiene los tipos de variables para una función"""
    var_types = {}
    
    # Tipos de argumentos
    for arg_list, tipo in func_info['args']:
        for arg in arg_list:
            var_types[arg] = tipo
    
    # Tipos de variables locales
    for var_list, tipo in func_info['vars']:
        for var in var_list:
            var_types[var] = tipo
    
    return var_types

def compile_expr(expr, var_map, functions=None, is_function_context=False):
    code = []
    if isinstance(expr, tuple):
        if expr[0] == 'rel':
            op, left, right = expr[1], expr[2], expr[3]
            code += compile_expr(left, var_map, functions, is_function_context)
            code += compile_expr(right, var_map, functions, is_function_context)
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
            code += compile_expr(left, var_map, functions, is_function_context)
            code += compile_expr(right, var_map, functions, is_function_context)
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
            code += compile_expr(left, var_map, functions, is_function_context)
            code += compile_expr(right, var_map, functions, is_function_context)
            code.append('AND')
        elif expr[0] == 'or':
            _, left, right = expr
            code += compile_expr(left, var_map, functions, is_function_context)
            code += compile_expr(right, var_map, functions, is_function_context)
            code.append('OR')
        elif expr[0] == 'not':
            _, subexpr = expr
            code += compile_expr(subexpr, var_map, functions, is_function_context)
            code.append('NOT')
        elif expr[0] == 'array':
            _, array_name, index_expr = expr
            if isinstance(var_map[array_name], tuple):
                base_index, logical_start = var_map[array_name]
                if is_function_context:
                    code.append('PUSHFP')
                else:
                    code.append('PUSHGP')
                code.append(f'PUSHI {base_index}')
                code.append('PADD')
                code += compile_expr(index_expr, var_map, functions, is_function_context)
                code.append(f'PUSHI {logical_start}')
                code.append('SUB')
                code.append('LOADN')
            else:
                # Para strings: primero referencia, luego índice base 0
                if is_function_context:
                    code.append(f'PUSHL {var_map[array_name]}')
                else:
                    code.append(f'PUSHG {var_map[array_name]}')
                code += compile_expr(index_expr, var_map, functions, is_function_context)
                code.append('PUSHI 1')
                code.append('SUB')
                code.append('CHARAT')
        elif expr[0] == 'func':
            func_name, args = expr[1]
            func_name_lower = func_name.lower()
            
            # Funciones built-in
            if func_name_lower == 'length':
                arg = args[0]
                if is_function_context:
                    code.append(f'PUSHL {var_map[arg]}')
                else:
                    code.append(f'PUSHG {var_map[arg]}')
                code.append('STRLEN')
            # Llamadas a funciones definidas por el usuario
            elif functions and func_name in functions:
                # Apilar argumentos en orden (no inverso para llamadas de funciones)
                for arg in args:
                    if arg in var_map:
                        if is_function_context:
                            code.append(f'PUSHL {var_map[arg]}')
                        else:
                            code.append(f'PUSHG {var_map[arg]}')
                    else:
                        try:
                            val = int(arg)
                            code.append(f'PUSHI {val}')
                        except ValueError:
                            code.append(f'PUSHS "{arg}"')
                
                # Llamar a la función
                code.append(f'PUSHA {func_name}')
                code.append('CALL')
            else:
                code.append(f'# Unsupported function: {func_name}')
        else:
            code.append(f'# Unsupported expr type: {expr}')
    elif isinstance(expr, str):
        if expr == 'true':
            code.append('PUSHI 1')
        elif expr == 'false':
            code.append('PUSHI 0')
        elif expr in var_map:
            if is_function_context:
                code.append(f'PUSHL {var_map[expr]}')
            else:
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

def compile_instr(instr, var_map, var_types, label_counter, functions=None, func_name=None):
    code = []
    is_function_context = func_name is not None
    
    if instr[0] == 'func':
        func_name_call, args = instr[1]
        func_name_lower = func_name_call.lower()
        
        if func_name_lower == 'write':
            for arg in args:
                if arg in var_map:
                    if is_function_context:
                        code.append(f'PUSHL {var_map[arg]}')
                    else:
                        code.append(f'PUSHG {var_map[arg]}')
                    # Determinar el tipo para usar la instrucción correcta
                    var_type = var_types.get(arg, 'integer')
                    if var_type == 'string':
                        code.append('WRITES')
                    else:
                        code.append('WRITEI')
                else:
                    code.append(f'PUSHS "{arg}"')
                    code.append('WRITES')
        elif func_name_lower == 'writeln':
            for arg in args:
                if arg in var_map:
                    if is_function_context:
                        code.append(f'PUSHL {var_map[arg]}')
                    else:
                        code.append(f'PUSHG {var_map[arg]}')
                    # Determinar el tipo para usar la instrucción correcta
                    var_type = var_types.get(arg, 'integer')
                    if var_type == 'string':
                        code.append('WRITES')
                    else:
                        code.append('WRITEI')
                else:
                    code.append(f'PUSHS "{arg}"')
                    code.append('WRITES')
            code.append('WRITELN')
        elif func_name_lower == 'readln':
            var = args[0]
            if isinstance(var, tuple) and var[0] == 'array':
                _, array_name, index_expr = var
                base_index, logical_start = var_map[array_name]
                if is_function_context:
                    code.append('PUSHFP')
                else:
                    code.append('PUSHGP')
                code.append(f'PUSHI {base_index}')
                code.append('PADD')
                code += compile_expr(index_expr, var_map, functions, is_function_context)
                code.append(f'PUSHI {logical_start}')
                code.append('SUB')
                code.append('READ')
                code.append('ATOI')
                code.append('STOREN')
            else:
                tipo = var_types.get(var, None)
                if tipo == 'string':
                    code.append('READ')
                    if is_function_context:
                        code.append(f'STOREL {var_map[var]}')
                    else:
                        code.append(f'STOREG {var_map[var]}')
                else:
                    code.append('READ')
                    code.append('ATOI')
                    if is_function_context:
                        code.append(f'STOREL {var_map[var]}')
                    else:
                        code.append(f'STOREG {var_map[var]}')
        # Llamadas a funciones definidas por el usuario (sin valor de retorno)
        elif functions and func_name_call in functions:
            # Apilar argumentos
            for arg in args:
                if arg in var_map:
                    if is_function_context:
                        code.append(f'PUSHL {var_map[arg]}')
                    else:
                        code.append(f'PUSHG {var_map[arg]}')
                else:
                    try:
                        val = int(arg)
                        code.append(f'PUSHI {val}')
                    except ValueError:
                        code.append(f'PUSHS "{arg}"')
            
            # Llamar a la función
            code.append(f'PUSHA {func_name_call}')
            code.append('CALL') 
            # Descartar el valor de retorno si no se usa
            code.append('POP 1')
        else:
            code.append(f'# Unsupported function: {func_name_call}')
    elif instr[0] == 'atrib':
        _, var, expr = instr
        code += compile_expr(expr, var_map, functions, is_function_context)
        
        # Almacenar el resultado
        if is_function_context:
            code.append(f'STOREL {var_map[var]}')
        else:
            code.append(f'STOREG {var_map[var]}')
    elif instr[0] == 'if':
        cond = next(x[1] for x in instr[1] if x[0] == 'cond')
        then_block = next(x[1] for x in instr[1] if x[0] == 'then')

        label_end = f'label{label_counter[0]}'
        label_counter[0] += 1

        code += compile_expr(cond, var_map, functions, is_function_context)
        code.append(f'JZ {label_end}')

        for i in then_block if isinstance(then_block, list) else [then_block]:
            code += compile_instr(i, var_map, var_types, label_counter, functions, func_name)

        code.append(f'{label_end}:')
    elif instr[0] == 'if_else':
        cond = next(x[1] for x in instr[1] if x[0] == 'cond')
        then_block = next(x[1] for x in instr[1] if x[0] == 'then')
        else_block = next(x[1] for x in instr[1] if x[0] == 'else')

        label_else = f'label{label_counter[0]}'
        label_end = f'label{label_counter[0] + 1}'
        label_counter[0] += 2

        code += compile_expr(cond, var_map, functions, is_function_context)
        code.append(f'JZ {label_else}')

        for i in then_block if isinstance(then_block, list) else [then_block]:
            code += compile_instr(i, var_map, var_types, label_counter, functions, func_name)
        code.append(f'JUMP {label_end}')

        code.append(f'{label_else}:')
        for i in else_block if isinstance(else_block, list) else [else_block]:
            code += compile_instr(i, var_map, var_types, label_counter, functions, func_name)
        code.append(f'{label_end}:')
    elif instr[0] == 'for':
        inicio = next(x[1] for x in instr[1] if x[0] == 'inicio')
        fim = next(x[1] for x in instr[1] if x[0] == 'fim')
        conteudo = next(x[1] for x in instr[1] if x[0] == 'conteudo')

        label_start = f'label{label_counter[0]}'
        label_end = f'label{label_counter[0] + 1}'
        label_counter[0] += 2

        code += compile_instr(inicio, var_map, var_types, label_counter, functions, func_name)
        code.append(f'{label_start}:')

        if is_function_context:
            code.append(f'PUSHL {var_map[inicio[1]]}')
        else:
            code.append(f'PUSHG {var_map[inicio[1]]}')
        code += compile_expr(fim, var_map, functions, is_function_context)
        code.append('SUPEQ')  # Cambiado de INFEQ a SUPEQ para verificar si hemos pasado el límite
        code.append(f'JZ {label_end}')

        if isinstance(conteudo, list):
            for instr_interno in conteudo:
                code += compile_instr(instr_interno, var_map, var_types, label_counter, functions, func_name)
        else:
            code += compile_instr(conteudo, var_map, var_types, label_counter, functions, func_name)
            
        if is_function_context:
            code.append(f'PUSHL {var_map[inicio[1]]}')
        else:
            code.append(f'PUSHG {var_map[inicio[1]]}')
        code.append('PUSHI 1')
        code.append('ADD')
        if is_function_context:
            code.append(f'STOREL {var_map[inicio[1]]}')
        else:
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

        code += compile_instr(inicio, var_map, var_types, label_counter, functions, func_name)
        code.append(f'{label_start}:')

        if is_function_context:
            code.append(f'PUSHL {var_map[inicio[1]]}')
        else:
            code.append(f'PUSHG {var_map[inicio[1]]}')
        code += compile_expr(fim, var_map, functions, is_function_context)
        code.append('INF')  # Cambiado de SUPEQ a INF para verificar si hemos pasado el límite inferior
        code.append(f'JZ {label_end}')

        if isinstance(conteudo, list):
            for instr_interno in conteudo:
                code += compile_instr(instr_interno, var_map, var_types, label_counter, functions, func_name)
        else:
            code += compile_instr(conteudo, var_map, var_types, label_counter, functions, func_name)

        if is_function_context:
            code.append(f'PUSHL {var_map[inicio[1]]}')
        else:
            code.append(f'PUSHG {var_map[inicio[1]]}')
        code.append('PUSHI 1')
        code.append('SUB')
        if is_function_context:
            code.append(f'STOREL {var_map[inicio[1]]}')
        else:
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
        code += compile_expr(cond, var_map, functions, is_function_context)
        code.append(f'JZ {label_end}')

        if isinstance(conteudo, list):
            for instr_interno in conteudo:
                code += compile_instr(instr_interno, var_map, var_types, label_counter, functions, func_name)
        else:
            code += compile_instr(conteudo, var_map, var_types, label_counter, functions, func_name)

        code.append(f'JUMP {label_start}')
        code.append(f'{label_end}:')
    else:
        code.append(f'# Unsupported instruction: {instr}')
    return code

def compile_function(func_name, func_info, functions, global_label_counter):
    """Compila una función individual"""
    code = []
    
    # Etiqueta de la función
    code.append(f'{func_name}:')
    
    # Crear mapa de variables y tipos para esta función
    func_var_map, total_vars = get_function_var_map(func_info, func_name)
    func_var_types = get_function_var_types(func_info)
    
    # Añadir el tipo de retorno para la variable del mismo nombre que la función
    func_var_types[func_name] = func_info['return_type']
    
    # Reservar espacio para variables locales
    num_args = sum(len(arg_list) for arg_list, _ in func_info['args'])
    local_vars = total_vars - num_args
    
    if local_vars > 0:
        code.append(f'PUSHN {local_vars}')
    
    # Compilar el cuerpo de la función
    for instr in func_info['body']:
        code += compile_instr(instr, func_var_map, func_var_types, global_label_counter, functions, func_name)
    
    # Retornar el valor (debe estar en la variable con el nombre de la función)
    if func_name in func_var_map:
        code.append(f'PUSHL {func_var_map[func_name]}')
    else:
        code.append('PUSHI 0')  # Valor por defecto si no se asignó
    
    code.append('RETURN')
    
    return code

def compile_to_maq(ast):
    maq_code = []
    
    # Obtener información de funciones
    functions = get_function_info(ast)
    
    # Variables globales
    var_map = get_var_index(ast)
    var_types = get_var_types(ast)
    label_counter = [0]

    # Programa principal
    maq_code.append('START')
    
    # Saltar las definiciones de funciones al inicio
    if functions:
        maq_code.append('JUMP main')
    
    # Compilar funciones
    for func_name, func_info in functions.items():
        maq_code += compile_function(func_name, func_info, functions, label_counter)
    
    # Programa principal
    if functions:
        maq_code.append('main:')
    
    # Inicializar variables globales
    if len(var_map) > 0:
        maq_code.append(f'PUSHN {len(var_map)}')

    # Compilar cuerpo principal
    corpo = next((v for (k, v) in ast if k == 'corpo'), [])
    for instr in corpo:
        maq_code += compile_instr(instr, var_map, var_types, label_counter, functions)

    maq_code.append('STOP')
    return maq_code


# -------- EJEMPLO DE USO ----------

if __name__ == '__main__':
    programa = [('nome_programa', 'BinarioParaInteiro'),
     ('functions',
      [('nome_function', 'BinToInt'),
       ('argsFunction', [(['bin'], 'string')]),
       ('tipoFunction', 'integer'),
       ('varsFunction', [(['i', 'valor', 'potencia'], 'integer')]),
       ('corpoFunction',
        [('atrib', 'valor', '0'),
         ('atrib', 'potencia', '1'),
         ('for_downto',
          [('inicio', ('atrib', 'i', ('func', ('length', ['bin'])))),
           ('fim', '1'),
           ('conteudo',
            [('if',
              [('cond', ('rel', '=', ('array', 'bin', 'i'), '1')),
               ('then',
                [('atrib', 'valor', ('binop', '+', 'valor', 'potencia'))])]),
             ('atrib', 'potencia', ('binop', '*', 'potencia', '2'))])]),
         ('atrib', 'BinToInt', 'valor')])]),
     ('vars', [(['bin'], 'string'), (['valor'], 'integer')]),
     ('corpo',
      [('func', ('writeln', ['Introduza uma string binaria:'])),
       ('func', ('readln', ['bin'])),
       ('atrib', 'valor', ('func', ('BinToInt', ['bin']))),
       ('func', ('writeln', ['O valor inteiro correspondente e: ', 'valor']))])]

    codigo = compile_to_maq(programa)
    print('\n'.join(codigo))