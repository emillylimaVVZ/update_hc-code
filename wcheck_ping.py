import subprocess
import webbrowser
import os
import json
from concurrent.futures import ThreadPoolExecutor
# Definir os endereços e descrições
addresses = [
   {"address": "10.34.111.254", "description": "Gateway Interno"},
   {"address": "10.34.0.100", "description": "Servidor de nomes Interno"},
   {"address": "www.uol.com.br", "description": "UOL Externo"},
   {"address": "aghu.hc-ufpe.ebserh", "description": "Servidor AGHU Interno"}
]
def ping_and_analyze(address):
   import subprocess
   try:
       response = subprocess.check_output(['ping', '-n', '15', address["address"]], text=True, stderr=subprocess.STDOUT, shell=True)
       lines = response.split('\r\n')
       # Vamos inicializar average_time como 'N/A' para casos em que não encontramos nenhum valor válido
       average_time = 'N/A'
       # Agora, ao invés de procurar uma linha específica, vamos procurar o último valor em ms no output completo
       for line in reversed(lines):  # Inverte a ordem das linhas para começar do final
           if 'ms' in line:
               # Extrai todos os pedaços de texto que terminam com 'ms'
               parts = line.split(' ')
               for part in parts:
                   if part.endswith('ms'):
                       average_time = part
                       break  # Sai do loop interno
               if average_time != 'N/A':
                   break  # Sai do loop externo se encontrarmos um valor de tempo
       # Encontrar a linha que contém a porcentagem de perda de pacotes
       packet_loss_line = next((line for line in lines if "perda" in line), None)
       packet_loss = '100%'
       if packet_loss_line:
           parts = packet_loss_line.split('(')
           packet_loss = parts[-1].split('%')[0]
       return {"address": address["address"], "description": address["description"], "avg_time": average_time, "packet_loss": packet_loss}
   except subprocess.CalledProcessError as e:
       return {"address": address["address"], "description": address["description"], "avg_time": 'N/A', "packet_loss": '100%'}
# Usar ThreadPoolExecutor para executar ping nos endereços em paralelo
results = {}
with ThreadPoolExecutor(max_workers=len(addresses)) as executor:
   future_to_address = {executor.submit(ping_and_analyze, address): address for address in addresses}
   for future in future_to_address:
       result = future.result()
       results[result["address"]] = result
corrected_avg_time_data = []
for data in results.values():
   try:
       # Tentar converter o tempo médio para float, após remover 'ms' e espaços em branco
       avg_time = data['avg_time'].replace('ms', '').strip()
       corrected_avg_time_data.append(float(avg_time) if avg_time != 'N/A' else 0)
   except ValueError:
       # Caso a conversão falhe por outro motivo, defina como 0 também
       corrected_avg_time_data.append(0)
# A mesma abordagem para os dados de perda de pacotes
corrected_packet_loss_data = []
for data in results.values():
   try:
       # Tentar converter a perda de pacotes para float, após remover '%' e espaços em branco
       packet_loss = data['packet_loss'].replace('% perda', '').strip()
       corrected_packet_loss_data.append(float(packet_loss) if packet_loss != '100% perda' else 100)
   except ValueError:
       # Caso a conversão falhe por outro motivo, defina como 100 também (assumindo perda total)
       corrected_packet_loss_data.append(100)
import subprocess
def get_netstat_results():
   try:
       # Execute o comando netstat com a opção que retorna estatísticas da interface de rede
       result = subprocess.check_output(['netstat', '-e'], text=True, stderr=subprocess.STDOUT, shell=True)
       lines = result.split('\n')  # Divide a saída em linhas
       netstat_results = {
           'bytes_received': None,
           'bytes_sent': None,
           'unicast_packets_received': None,
           'unicast_packets_sent': None,
           'non_unicast_packets_received': None,
           'non_unicast_packets_sent': None,
           'discarded_packets_received': None,
           'discarded_packets_sent': None,
           'errors_received': None,
           'errors_sent': None,
       }
       # Mapear cada linha com as respectivas colunas de acordo com a saída
       for line in lines:
           if 'Bytes' in line:
               values = line.split()
               netstat_results['bytes_received'] = int(values[1].replace('.', ''))
               netstat_results['bytes_sent'] = int(values[2].replace('.', ''))
           elif 'Unicast' in line:
               values = line.split()
               netstat_results['unicast_packets_received'] = int(values[2].replace('.', ''))
               netstat_results['unicast_packets_sent'] = int(values[3].replace('.', ''))
           if 'Não-Unicast' in line:
               values = line.split()
               netstat_results['non_unicast_packets_received'] = int(values[3].replace('.', ''))
               netstat_results['non_unicast_packets_sent'] = int(values[4].replace('.', ''))
           elif 'Pacotes Descartados' in line:
               values = line.split()
               netstat_results['discarded_packets_received'] = int(values[1].replace('.', ''))
               netstat_results['discarded_packets_sent'] = int(values[2].replace('.', ''))
           if 'Erros' in line:
               values = line.split()
               netstat_results['errors_received'] = int(values[1].replace('.', ''))
               netstat_results['errors_sent'] = int(values[2].replace('.', ''))
       return netstat_results
   except subprocess.CalledProcessError as e:
       print(f"Erro ao executar o comando netstat -e: {e}")
       return None
netstat_results = get_netstat_results()
# Gerar conteúdo HTML com JavaScript incorporado para Chart.js, incluindo traduções para o Português
html_content = f"""
<!DOCTYPE html>
<html>
<head>
<title>Resultados do Ping</title>
<link rel="shortcut icon" type="image/png" href="https://drive.google.com/file/d/1gtvlcKu2YV_pl6GRLfnzh5fqfY-KlWJI/view?usp=sharing">
<link rel="stylesheet" type="text/css" href="styles.css">  
</head>
<body>
<header>
<div id="menu">
<div id="menu-bar" onclick="menuOnClick()">
<div id="bar1" class="bar"></div>
<div id="bar2" class="bar"></div>
<div id="bar3" class="bar"></div>
</div>
<nav class="nav" id="nav">
<ul>
<li><a href="#">Home</a></li>
<li><a href="#">Contato</a></li>
</ul>
</nav>
</div>
<div class="menu-bg" id="menu-bg"></div>
<div id="support">
<i class="fas fa-headphones"></i> Suporte
</div>
</header>
<h1>Resultados do Ping</h1>
<table>
<tr>
<th>Endereço</th>
<th>Descrição</th>
<th>Latência Média (ms)</th>
<th>Perda de Pacotes (%)</th>                      
</tr>
       {"".join([f"<tr><td>{data['address']}</td><td>{data['description']}</td><td class='avg-time'>{data['avg_time']}</td><td class='packet-loss'>{data['packet_loss']}</td></tr>" for data in results.values()])}    
</table>
<h2>Estatísticas de Interface</h2>
<table>
<tr>
<th>Atributo</th>
<th>Recebidos</th>
<th>Enviados</th>
</tr>
<tr>
<td>Bytes</td>
<td>{netstat_results['bytes_received']}</td>
<td>{netstat_results['bytes_sent']}</td>
</tr>
<tr>
<td>Unicast</td>
<td>{netstat_results['unicast_packets_received']}</td>
<td>{netstat_results['unicast_packets_sent']}</td>
</tr>
<tr>
<td>Não-Unicast</td>
<td>{netstat_results['non_unicast_packets_received']}</td>
<td>{netstat_results['non_unicast_packets_sent']}</td>
</tr>
<tr>
<td>Discarded</td>
<td>{netstat_results['discarded_packets_received']}</td>
<td>{netstat_results['discarded_packets_sent']}</td>
</tr>
<tr>
<td>Erros</td>
<td>{netstat_results['errors_received']}</td>
<td>{netstat_results['errors_sent']}</td>
</tr>
</table>
<div id="info-box">
<p>Caso a perda de pacotes ultrapasse 80%, contate o suporte de TI.</p>
<p>A sinalização verde aponta um bom fluxo de rede.</p>
</div>
<script src="script.js"></script>
</body>
</html>
"""
with open("netstat_results.html", "w") as f:
   f.write(html_content)
# Salvar em arquivo HTML e abrir no navegador padrão
file_path = 'ping_results.html'
with open(file_path, 'w') as file:
   file.write(html_content)
webbrowser.open('file://' + os.path.realpath(file_path))
