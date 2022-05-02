import sys # Leer argumentos desde línea de comandos.
import re
import math

archivoDeDocumentos = sys.argv[1]
# archivoDeConsultas = sys.argv[2]

palabrasVacias = []
archivo = open("palabrasVacias.txt", "r", encoding="utf8")
for linea in archivo:
    palabrasVacias.append(linea.replace("\n", ""))
archivo.close()

sufijos = []
archivo = open("sufijos.txt", "r", encoding="utf8")
for linea in archivo:
    sufijos.append(linea.replace("\n", ""))
archivo.close()

terminosTotales = []
periodicos = []
noticias = []
cuerpos = []
documentos = []

# Se leen los documentos (en este caso, las frases).
archivo = open(archivoDeDocumentos, "r")
dentroDelCuerpo = False

temp = []

for linea in archivo:
	if ('<periodico>' in linea.split()):
		lineaProcesada = re.sub(r"[:|.|_|...|&|-|%|{|}|*|/|¿|?|,|;|(|)|<<|>>|'|*|¡|!]", r' ', linea)
		terminosEnLinea = lineaProcesada.split(" ")
		while ('' in terminosEnLinea):
			terminosEnLinea.remove('')
		while ("periodico" in terminosEnLinea):
			terminosEnLinea.remove('periodico')
		while ('\n' in terminosEnLinea):
			terminosEnLinea.remove('\n')
		#print(terminosEnLinea)
	
	if ('<noticia>' in linea.split()):
		lineaProcesada = re.sub(r"[:|.|_|...|&|-|%|{|}|*|/|¿|?|,|;|(|)|<<|>>|'|*|¡|!]", r' ', linea)
		terminosEnLinea = lineaProcesada.split(" ")
		while ('' in terminosEnLinea):
			terminosEnLinea.remove('')
		while ("noticia" in terminosEnLinea):
			terminosEnLinea.remove('noticia')
		while ('\n' in terminosEnLinea):
			terminosEnLinea.remove('\n')
		#print(terminosEnLinea)
	
	if ('<noticias>' in linea.split()):
		lineaProcesada = re.sub(r"[:|.|_|...|&|-|%|{|}|*|/|¿|?|,|;|(|)|<<|>>|'|*|¡|!]", r' ', linea)
		terminosEnLinea = lineaProcesada.split(" ")
		while ('' in terminosEnLinea):
			terminosEnLinea.remove('')
		while ("noticias" in terminosEnLinea):
			terminosEnLinea.remove('noticias')
		while ('\n' in terminosEnLinea):
			terminosEnLinea.remove('\n')
		#print(terminosEnLinea)

	if (dentroDelCuerpo):
		if ('</cuerpo>' not in linea.split()):
			temp.append(linea.split())
		#print(temp)
	else:
		temp = []

	if ('<cuerpo>' in linea.split()):
		dentroDelCuerpo = True

	if ('</cuerpo>' in linea.split()):
		cuerpos.append(list(filter(None, temp)))
		dentroDelCuerpo = False
archivo.close()

print(len(cuerpos))
	
for cuerpo in cuerpos:
	lineaTemp = []
	for linea in cuerpo:
		for palabra in linea:
			palabraProcesada = re.sub(r"[:|.|_|...|&|-|%|{|}|*|/|¿|?|,|;|(|)|<<|>>|'|*|¡|!]", r'', palabra)
			palabraProcesada = palabraProcesada.replace('"', "")
			palabraProcesada = palabraProcesada.replace('-', "")
			palabraProcesada = palabraProcesada.lower()
			if palabraProcesada in palabrasVacias:
				continue
			for sufijo in sufijos:
				if (palabraProcesada.endswith(sufijo)):
					palabraProcesada = palabraProcesada[:-(len(sufijo))]
					lineaTemp.append(palabraProcesada)
					terminosTotales.append(palabraProcesada)
					break
	documentos.append(lineaTemp)

#for cuerpoProcesado in cuerposProcesados:
	#print(cuerpoProcesado)

N = len(documentos)

terminosTotales = list(set(terminosTotales))

matrizTF = []
matrizIDF = []

# Se realiza el cálculo de las matrices de TF y de IDF.
for termino in terminosTotales:
	frecuenciaDocumento = 0 
	filaTF = []
	for documento in documentos:
		aparicionesDelTerminoEnDocumento = documento.count(termino)
		frecuenciaTermino = 0
		if(aparicionesDelTerminoEnDocumento > 0):
			frecuenciaTermino = 1 + math.log2(aparicionesDelTerminoEnDocumento)
		filaTF.append(frecuenciaTermino)
		if(termino in documento):
			frecuenciaDocumento += 1
	matrizTF.append(filaTF)
	frecuenciaDocumentoInversa = math.log2(N / frecuenciaDocumento)
	matrizIDF.append(frecuenciaDocumentoInversa)

matrizTFIDF = []

# Se realiza el cálculo de los valores de la matriz TF/IDF.
for indice, arregloTF in enumerate(matrizTF):
	filaTFIDF = []
	filaTFIDF.append(terminosTotales[indice])
	for valorTF in arregloTF:
		tfidf = valorTF * matrizIDF[indice]
		filaTFIDF.append(tfidf)
	matrizTFIDF.append(filaTFIDF)

# Se realiza el cálculo de los valores de los vectores normalizados para cada documento.
vectorNormalizado = []
for columna in range (0, N):
	sumatoria = 0
	for fila in matrizTFIDF:
		if (fila[columna + 1] > 0):
			sumatoria = sumatoria + (math.pow(fila[columna + 1], 2))
	resultado = math.sqrt(sumatoria)
	vectorNormalizado.append(resultado)

#print(vectorNormalizado)

# Función para determinar el ángulo entre los vectores. Los parámetros recibidos son los números de los documentos a valorar.
def anguloEntre(documentoA, documentoB):
	productoPunto = 0
	for fila in matrizTFIDF:
		if (fila[documentoA] > 0 and fila[documentoB] > 0):
			productoPunto = productoPunto + (fila[documentoA] * fila[documentoB])
	cosDelAngulo = 0
	if (vectorNormalizado[documentoA - 1] > 0 and vectorNormalizado[documentoB - 1] > 0):
		cosDelAngulo = productoPunto / (vectorNormalizado[documentoA - 1] * vectorNormalizado[documentoB - 1])
	return cosDelAngulo

# Aquí se compararán las consultas con los documentos, se ordenarán los resultados por rango y luego se imprimirán.
for consulta in range(0, 5):
	resultados = {}
	for documento in range(1, N - 4):
		similitud = anguloEntre((N - 4) + consulta, documento)
		if(similitud > 0):
			resultados[documento] = similitud
	resultadosOrdenados = sorted(resultados.items(), key=lambda x: x[1], reverse = True)

	print("Modelo de Espacio Vectorial para la consulta \'", end = "")
	for _ in documentos[(N - 5) + consulta]:
		print(_, end = " ")
	print("\':")
	for indice, (llave, valor) in enumerate(resultadosOrdenados):
		if(indice < 5):
			print("\td", llave, ":\t", "{:.3}".format(valor), "-", end = "")
			for _ in documentos[llave - 1]:
				print(_, end = " ")
			print("")
	print("")

matrizDeSimilitud = []

for i in range (0, N):
	temp = []
	for j in range (0, N):
		temp.append(0)
	matrizDeSimilitud.append(temp)


for i in range (0, N):
	for j in range (i + 1, N):
		matrizDeSimilitud[i][j] = anguloEntre(i + 1, j + 1)
		print("(", i + 1, ",", j + 1, "): ", matrizDeSimilitud[i][j])

#for li in matrizDeSimilitud:
#	for value in li:
#		print("\t", value, end = "")
#	print("")
#print(matrizDeSimilitud)