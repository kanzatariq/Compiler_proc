@"
import sys
import subprocess
from lexer import tokenize
from parser import Parser
from semantic import SemanticAnalyzer
from ir_gen import IRGenerator
from codegen import CodeGenerator

def compile_file(path):
    with open(path) as f:
        source = f.read()
    print(f'[1] Lexing {path}...')
    tokens = tokenize(source)
    print('[2] Parsing...')
    ast = Parser(tokens).parse()
    print('[3] Semantic analysis...')
    SemanticAnalyzer().analyze(ast)
    print('[4] Generating IR...')
    ir = IRGenerator().gen(ast)
    print('[5] Optimizing...')
    print('[6] Generating C code...')
    c_code = CodeGenerator().generate(ir)
    out_c = path.replace('.par', '.c')
    out_bin = path.replace('.par', '.exe')
    with open(out_c, 'w') as f:
        f.write(c_code)
    print(f'    Written: {out_c}')
    print('[7] Compiling C to binary...')
    result = subprocess.run(['gcc', out_c, '-o', out_bin], capture_output=True, text=True)
    if result.returncode != 0:
        print('GCC Error:')
        print(result.stderr)
        sys.exit(1)
    print(f'    Binary: {out_bin}')
    print('\n✓ Compilation successful!')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python src/main.py <file.par>')
        sys.exit(1)
    compile_file(sys.argv[1])
"@ | Set-Content src/main.py