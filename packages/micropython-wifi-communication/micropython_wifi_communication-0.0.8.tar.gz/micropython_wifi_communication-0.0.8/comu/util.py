
def validator(item):
    item = item.split('0: 0}')
    item = item[len(item) - 2] + '0: 0}'
    try:
        item = eval(item)
    except:
        return True, False
    x = False
    y = False
    try:
        item[1]
    except:
        x = True
    try:
        item[0]
    except:
        y = True
    if x or y:
        return True, False
    return False, item

def get_ip_and_netmask_in_windos():
    import subprocess
    import re
    # Executa o comando ipconfig
    output = subprocess.check_output('ipconfig', shell=True).decode('latin-1')
    output = output.split('Adaptador de Rede sem Fio Wi-Fi:')[1]

    # Procura pelo endereço IP da rede e pela máscara de rede na saída
    ip_regex = r"IPv4. .+?: ([\d.]+)"
    mask_regex = r"Sub-rede . .+?: ([\d.]+)"

    ip_match = re.search(ip_regex, output)
    mask_match = re.search(mask_regex, output)

    if ip_match and mask_match:
        ip_address = ip_match.group(1)
        netmask = mask_match.group(1)

        return ip_address, netmask

    return None, None  # Retorna None se não encontrou as informações

def ip(host,ipmsk=None,se=None):
    host1 = None
    mask1 = None
    host2 = None
    mask2 = None
    if ipmsk:
        if type(ipmsk) == tuple:
            host1, mask1, host2, mask2 = ipmsk
    else:
        host1, mask1 = get_ip_and_netmask_in_windos()
        host2 = host1
        mask2 = mask1
        if se:
            print(f'Host para ser adicionado no esp32: {host1}')
            return (host1,mask1,host1,mask1)
    mascara = mask1.split('.')
    hostpadrao = host1.split('.')
    ipfinal = ''
    x = 0
    espasos = 0
    for i in mascara:
        i = int(i)
        if i == 255:
            ipfinal+=f'{str(hostpadrao[x])}.'
        else:
            espasos+=1
        x+=1
    host = host.split('.')
    for i in range(len(host)-1):
        if not espasos == len(host):
            del host[0]
    x=1
    for i in host:
        if x == len(host):
            ipfinal+=i
        else:
            ipfinal+=i+'.'
        x+=1
    return (ipfinal,mask1,ipfinal,mask1)