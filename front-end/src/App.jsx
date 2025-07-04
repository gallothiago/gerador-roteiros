import { useState, useEffect, useRef } from 'react';
import useTravelGenerator from './hooks/useTravelGenerator'; // Garanta que o caminho está correto
import TravelForm from './components/TravelForm';
import RoteiroDisplay from './components/RoteiroDisplay';
import './App.css';

function App() {
    // DESESTRUTURAR APENAS AS FUNÇÕES E ESTADOS EXPOSTOS PELO HOOK
    const { roteiro, loading, error, backendStatus, generateRoteiro, resetRoteiro } = useTravelGenerator();

    const [currentDestination, setCurrentDestination] = useState('');
    const [showSuccessMessage, setShowSuccessMessage] = useState(false);
    const [budgetSuggestion, setBudgetSuggestion] = useState('');

    const roteiroRef = useRef(null);

    const handleFormSubmit = async (travelData) => {
        setBudgetSuggestion('');
        setCurrentDestination(travelData.destino);

        await generateRoteiro(travelData);
        
        // Verificação para mostrar mensagem de sucesso
        // Se há um roteiro OU uma sugestão de orçamento vindo do backend (mesmo que roteiro seja vazio mas a sugestão exista)
        if (roteiro || (backendStatus && backendStatus.includes("rodando!"))) { 
            setShowSuccessMessage(true);
            // Verifica se roteiro existe antes de tentar acessar .sugestao_orcamento
            setBudgetSuggestion(roteiro?.sugestao_orcamento || ''); 
        } else {
            setShowSuccessMessage(false);
        }
    };

    const handleClearRoteiro = () => {
        resetRoteiro(); // Chame a função de reset do hook
        setShowSuccessMessage(false);
        setBudgetSuggestion('');
        setCurrentDestination('');
    };

    useEffect(() => {
        if (roteiro && roteiroRef.current) {
            roteiroRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [roteiro]);

    return (
        <div className="app-container">
            <header className="app-header">
                <h1>Gerador de Roteiros de Viagem</h1>
                <p className="backend-status">{backendStatus}</p>
            </header>
            <main className="app-main">
                <TravelForm
                    onSubmit={handleFormSubmit}
                    loading={loading}
                    currentDestination={currentDestination}
                />
                {error && <p className="error-message">{error}</p>}
                
                {showSuccessMessage && !error && (
                    <div className="success-message">
                        <p>Seu roteiro foi gerado com sucesso!</p>
                        {budgetSuggestion && <p>{budgetSuggestion}</p>}
                    </div>
                )}

                {loading && <p className="loading-message">Gerando seu roteiro, por favor aguarde...</p>}
                
                {roteiro && (
                    <div ref={roteiroRef} className="roteiro-section">
                        <h2>Seu Roteiro Sugerido:</h2>
                        {/* Verifique se roteiro.roteiro existe antes de passar para RoteiroDisplay */}
                        {roteiro.roteiro && <RoteiroDisplay roteiro={roteiro.roteiro} />}
                        <button onClick={handleClearRoteiro} className="clear-button">
                            Limpar Roteiro e Começar de Novo
                        </button>
                    </div>
                )}
            </main>
        </div>
    );
}

export default App;