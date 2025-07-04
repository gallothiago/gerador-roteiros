import { useState, useCallback, useEffect } from 'react';
import axios from 'axios'; // Garanta que axios está sendo importado corretamente

const useTravelGenerator = () => {
    const [roteiro, setRoteiro] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [backendStatus, setBackendStatus] = useState("Verificando status do backend...");

    // Verifica o status do backend ao carregar
    useEffect(() => {
        const checkBackendStatus = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/hello');
                setBackendStatus(`Status do Backend: ${response.data.message}`);
            } catch (err) {
                setBackendStatus("Status do Backend: Erro ao conectar.");
                console.error("Erro ao verificar status do backend:", err);
            }
        };
        checkBackendStatus();
    }, []);

    const generateRoteiro = useCallback(async (travelData) => {
        setLoading(true);
        setError(null);
        setRoteiro(null); // Limpa o roteiro anterior ao gerar um novo
        try {
            const response = await axios.post('http://127.0.0.1:5000/api/generate_roteiro', travelData);
            setRoteiro(response.data);
        } catch (err) {
            console.error("Erro ao gerar roteiro:", err);
            if (err.response && err.response.data && err.response.data.mensagem) {
                setError(`Erro ao carregar o roteiro: ${err.response.data.mensagem}`);
            } else {
                setError("Erro desconhecido ao gerar roteiro. Tente novamente.");
            }
            setRoteiro(null); // Limpar roteiro em caso de erro
        } finally {
            setLoading(false);
        }
    }, []);

    // Nova função para resetar o roteiro
    const resetRoteiro = useCallback(() => {
        setRoteiro(null);
        setError(null);
    }, []);

    return {
        roteiro,
        loading,
        error,
        backendStatus,
        generateRoteiro,
        resetRoteiro // Exponha a nova função de reset
    };
};

export default useTravelGenerator;