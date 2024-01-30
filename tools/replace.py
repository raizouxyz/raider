import glob

a = glob.glob('../raider/*.py') + glob.glob('../raider/*/*.py')
for b in a:
    with open(b, mode='r', encoding='utf-8') as f:
        code = f.read().replace("", "")
        with open(b, mode='w', encoding='utf-8') as f2:
            f2.write(code)