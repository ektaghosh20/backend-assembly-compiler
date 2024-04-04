def compile(code):
    from sys import exit
    motOpCode = {
        "MOV": 1,
        "A": 2,
        "S": 3,
        "M": 4,
        "D": 5,
        "AN": 6,
        "O": 7,
        "ADD": 8,
        "SUB": 9,
        "MUL": 10,
        "DIV": 11,
        "AND": 12,
        "OR": 13,
        "LOAD": 14,
        "STORE": 15,
        "DCR": 16,
        "INC": 17,
        "JMP": 18,
        "JNZ": 19,
        "HALT": 20
    }

    motSize = {
        "MOV": 1,
        "A": 1,
        "S": 1,
        "M": 1,
        "D": 1,
        "AN": 1,
        "O": 1,
        "ADD": 1,
        "SUB": 2,
        "MUL": 2,
        "DIV": 2,
        "AND": 2,
        "OR ": 2,
        "LOAD": 3,
        "STORE": 3,
        "DCR": 1,
        "INC": 1,
        "JMP": 3,
        "JNZ": 3,
        "HALT": 1
    }
    code_lines_list = code.splitlines()
    l = []
    relativeAddress = []
    machineCode = []
    symbol = []
    symbolValue = []
    RA = 0
    current = 0
    count = 0
    temp = []
    n = len(code_lines_list)
    
    try:
        for i in range(n):
            instructions = code_lines_list[i]
            l.append(instructions)
        l = [x.upper() for x in l]
        for i in range(n):
            x = l[i]
            if "NEXT:" in x:
                s1 = ''.join(x)
                a, b, c = s1.split()
                a = a[:4]
                l[i] = b + " " + c
                symbol.append(a)
                x = l[i]
                if b in motOpCode:
                    value = motOpCode.get(b)
                    size = motSize.get(b)
                    if len(str(size)) == 1:
                        temp = "000" + str(size)
                    elif len(str(size)) == 2:
                        temp = "00" + str(size)
                    elif len(str(size)) == 3:
                        temp = "0"+str(size)
                else:
                    return 'instruction is not in opcode'
                    exit(0)
                symbolValue.append(temp)
                previous = size
                RA += current
                current = previous
                relativeAddress.append(RA)
                if c.isalpha() is True:
                    machineCode.append(str(value))
                else:
                    temp = list(b)
                    for i in range(len(temp)):
                        if count == 2:
                            temp.insert(i, ',')
                            count = 0
                        else:
                            count = count + 1
                    s = ''.join(temp)
                    machineCode.append(str(value) + "," + s)
            elif " " in x:
                s1 = ''.join(x)
                a, b = s1.split()
                if a in motOpCode:
                    value = motOpCode.get(a)
                    size = motSize.get(a)
                    previous = size
                    RA += current
                    current = previous
                    relativeAddress.append(RA)
                    if b.isalpha() is True:
                        machineCode.append(str(value))
                    else:
                        temp = list(b)
                        for i in range(len(temp)):
                            if count == 2:
                                temp.insert(i, ',')
                                count = 0
                            else:
                                count = count + 1
                        s = ''.join(temp)
                        machineCode.append(str(value) + "," + s)
                else:
                    return 'instruction is not in opcode'
                    exit(0)
            else:
                if x in motOpCode:
                    value = motOpCode.get(x)
                    size = motSize.get(x)
                    previous = size
                    RA += current
                    current = previous
                    relativeAddress.append(RA)
                    machineCode.append(value)
                else:
                    return 'your output comes hear'
                    exit(0)
        output = ""

        output += "Symbol Table  :  \n\n"
        output += " Symbol           Value(Address)\n"
        for i in range(len(symbol)):
            output += " {}              {}\n".format(symbol[i], symbolValue[i])
        
        output += "\n Pass-1 machine code output without reference of the symbolic address : \n"
        output += "Relative Address	Instruction	    OpCode\n"
        for i in range(n):
            if "NEXT" in l[i]:
                output += "{}                                 {}	              {}, - \n".format(
                    relativeAddress[i], l[i], machineCode[i])
            else:
                output += "{}                                 {}	              {} \n".format(
                    relativeAddress[i], l[i], machineCode[i])
        
        output += "\n Pass-2 output: Machine code output \n "
        output += "Relative Address	    Instruction	            OpCode\n"
        for i in range(n):
            if "NEXT" in l[i]:
                for j in range(len(symbol)):
                    if "NEXT" in symbol[j]:
                        pos = j
                        output += "{}                                    {}	                 {} , {}\n".format(
                            relativeAddress[i], l[i], machineCode[i], symbolValue[pos])
            else:
                output += "{}                                       {}	                 {} \n".format(
                    relativeAddress[i], l[i], machineCode[i])
        
        return output

    except:
        return 'compilation error'


# from flask import Flask, render_template,request
# app = Flask(__name__)
# app = Flask(__name__, static_url_path='/static', static_folder='static')

# @app.route('/', methods=['GET', 'POST'])
# def index():
#    code=request.form.get('code','')
#    result=compile(code)
#    return render_template('index.html',result=result,code=code)


# if __name__ == '__main__':
#     app.run(debug=True)