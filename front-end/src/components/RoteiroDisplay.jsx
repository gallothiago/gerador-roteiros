import React from 'react';
import './RoteiroDisplay.css'; // Certifique-se de ter um CSS para isso ou adicione no App.css

const RoteiroDisplay = ({ roteiro, error }) => {
  if (error) {
    return <div className="error-message">Erro ao carregar o roteiro: {error}</div>;
  }

  if (!roteiro) {
    return null; // Não renderiza nada se não houver roteiro
  }

  return (
    <div className="roteiro-container">
      <h2>Seu Roteiro Sugerido:</h2>
      {roteiro.map((dia) => (
        <div key={dia.dia} className="dia-roteiro">
          <h3>Dia {dia.dia}</h3>
          <ul>
            {dia.atividades.map((atividade, index) => (
              // Usamos dangerouslySetInnerHTML porque o backend está enviando HTML para os links
              <li key={index} dangerouslySetInnerHTML={{ __html: atividade }}></li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default RoteiroDisplay;