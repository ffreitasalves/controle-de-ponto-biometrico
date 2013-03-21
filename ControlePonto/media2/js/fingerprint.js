// JavaScript Document
function registradigital()
{	
	var err, payload;
	var result = false;

	try // Tratamento de Exceções
	{
		DEVICE_AUTO_DETECT	= 255;
		
		var objNBioBSP = new ActiveXObject('NBioBSPCOM.NBioBSP.1');
		var objDevice = objNBioBSP.Device;
		var objExtraction = objNBioBSP.Extraction;		

		// Abrindo dispositivo [AUTO_DETECT]
		// O Dispositivo precisa estar aberto antes de adicionar um usuário
		objDevice.Open(DEVICE_AUTO_DETECT);

		err = objDevice.ErrorCode;	// Código do erro
		if ( err != 0 )		// Falha na abertura do dispositivo
		{
			alert('Falha na abertura do dispositivo: [' + err + ']');
		}
		else
		{
			// Adicionar digital de usuário
			objExtraction.Enroll(payload);
			err = objExtraction.ErrorCode;	// Código do erro.
		
			if ( err != 0 )		// Falha na adição de digital
			{
				alert('Falha no Registro: [' + err + ']');
			}
			else	// Registro com sucesso
			{
				// Pega o dado no formato texto
				alert('Registro efetuado com sucesso.');
				result = true;
				return objExtraction.TextEncodeFIR;
			}
			
			// Fechar dispositivos abertos.
			objDevice.Close(DEVICE_AUTO_DETECT);
		}

		objExtraction = 0;
		objDevice = 0;
		objNBioBSP = 0;		
	}
	catch(e)
	{
		alert(e.message);
		return(false);
	}
}

function capture()
{	
	var err;
	var result = false;
	
	try // tratamento de erros
	{
		DEVICE_AUTO_DETECT	= 255;
	
		var objNBioBSP = new ActiveXObject('NBioBSPCOM.NBioBSP.1');
		var objDevice = objNBioBSP.Device;
		var objExtraction = objNBioBSP.Extraction;

		// Abrir o dispositivo
		objDevice.Open(DEVICE_AUTO_DETECT);

		err = objDevice.ErrorCode;	// pega o nro do erro
		if ( err != 0 )		// Não achou o dispositivo
		{
			alert('Falha na Abertura do Dispositivo !');
			return(false);
		}
		else
		{
			// Pega a digital do usuário
			objExtraction.Capture();
			err = objExtraction.ErrorCode;	// pega o nro do erro
		
			if ( err != 0 )		// Se não pegou
			{
				alert('Falha na captura ! erro nro : [' + err + ']');
				return(false);
			}
			else	// Se deu certo
			{
				// Transforma a captura em texto
				result = objExtraction.TextEncodeFIR;
			}
		
			// fecha o dispositivo
			objDevice.Close(DEVICE_AUTO_DETECT);
		}
				
		objExtraction = 0;
		objDevice = 0;		
		objNBioBSP = 0;
	}
	catch(e)
	{
		alert(e.message);
		return(false);
	}
	
	return (result);
}

function compara(digi1, digi2)
{
	var err;
	var result = false;
	
	try // Tratamento de Erro
	{
		DEVICE_AUTO_DETECT	= 255;
	
		var objNBioBSP = new ActiveXObject('NBioBSPCOM.NBioBSP.1');
		var objCompara = objNBioBSP.Matching; //Setando um objeto de comparação (Classe Matching)

		//Comparando as digitais
		objCompara.VerifyMatch(digi1,digi2); 
		result = objCompara.MatchingResult //Acessando a propriedade de resultado do objeto comparação
		return result;
	}
		
	catch(e)
	{
		return("erro");
	}

	objNBioBSP = 0;
	objCompara = 0;
		
}