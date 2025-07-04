import React, { useState, forwardRef, useImperativeHandle } from 'react';

const TravelForm = forwardRef(({ onSubmit, loading }, ref) => {
  // Estados para os dados do formulário
  const [destino, setDestino] = useState('');
  const [dataInicio, setDataInicio] = useState('');
  const [dataFim, setDataFim] = useState('');
  const [orcamento, setOrcamento] = useState('');
  const [tipoViajante, setTipoViajante] = useState('');
  const [interesses, setInteresses] = useState([]);

  // >>> Novos estados para mensagens de erro de validação <<<
  const [errors, setErrors] = useState({});

  // Função interna para resetar todos os estados do formulário E os erros
  const resetForm = () => {
    setDestino('');
    setDataInicio('');
    setDataFim('');
    setOrcamento('');
    setTipoViajante('');
    setInteresses([]);
    setErrors({}); // Limpa os erros também
  };

  // Expõe a função 'resetForm' para o componente pai através da ref
  useImperativeHandle(ref, () => ({
    reset: resetForm
  }));

  // Função para lidar com a mudança das checkboxes de interesse
  const handleInteresseChange = (e) => {
    const { value, checked } = e.target;
    if (checked) {
      setInteresses(prevInteresses => [...prevInteresses, value]);
    } else {
      setInteresses(prevInteresses => prevInteresses.filter(interesse => interesse !== value));
    }
  };

  // >>> Nova função para validar o formulário antes de submeter <<<
  const validateForm = () => {
    const newErrors = {};
    if (!destino) newErrors.destino = 'O destino é obrigatório.';
    if (!dataInicio) newErrors.dataInicio = 'A data de início é obrigatória.';
    if (!dataFim) newErrors.dataFim = 'A data de fim é obrigatória.';
    if (!orcamento || parseFloat(orcamento) <= 0) newErrors.orcamento = 'O orçamento deve ser um número positivo.';
    if (!tipoViajante) newErrors.tipoViajante = 'O tipo de viajante é obrigatório.';

    // Validação de datas: data de início não pode ser depois da data de fim
    if (dataInicio && dataFim) {
      const start = new Date(dataInicio);
      const end = new Date(dataFim);
      if (start > end) {
        newErrors.dataFim = 'A data de fim não pode ser anterior à data de início.';
      }
    }

    setErrors(newErrors); // Atualiza o estado de erros
    return Object.keys(newErrors).length === 0; // Retorna true se não houver erros
  };

  // Função de submissão do formulário
  const handleSubmit = (e) => {
    e.preventDefault();
    setErrors({}); // Limpa erros anteriores ao tentar submeter

    if (!validateForm()) { // Se a validação falhar, não submete
      return;
    }

    const dadosViagem = {
      destino,
      dataInicio,
      dataFim,
      orcamento: parseFloat(orcamento),
      tipoViajante,
      interesses
    };
    onSubmit(dadosViagem); // Chama a função passada via props
  };

  return (
    <form onSubmit={handleSubmit} className="travel-form">
      <div className="form-group">
        <label htmlFor="destino">Destino:</label>
        <input
          type="text"
          id="destino"
          value={destino}
          onChange={(e) => setDestino(e.target.value)}
          placeholder="Ex: Paris, Roma, Maceió"
          required // Mantém o required para validação básica do navegador
          className={errors.destino ? 'input-error' : ''} // Adiciona classe para estilo de erro
        />
        {errors.destino && <p className="error-message-inline">{errors.destino}</p>} {/* Exibe erro */}
      </div>

      <div className="form-group date-group">
        <div className="date-item">
          <label htmlFor="dataInicio">Data de Início:</label>
          <input
            type="date"
            id="dataInicio"
            value={dataInicio}
            onChange={(e) => setDataInicio(e.target.value)}
            required
            className={errors.dataInicio ? 'input-error' : ''}
          />
          {errors.dataInicio && <p className="error-message-inline">{errors.dataInicio}</p>}
        </div>
        <div className="date-item">
          <label htmlFor="dataFim">Data de Fim:</label>
          <input
            type="date"
            id="dataFim"
            value={dataFim}
            onChange={(e) => setDataFim(e.target.value)}
            required
            className={errors.dataFim ? 'input-error' : ''}
          />
          {errors.dataFim && <p className="error-message-inline">{errors.dataFim}</p>}
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="orcamento">Orçamento Estimado (R$):</label>
        <input
          type="number"
          id="orcamento"
          value={orcamento}
          onChange={(e) => setOrcamento(e.target.value)}
          placeholder="Ex: 2000"
          min="0"
          required
          className={errors.orcamento ? 'input-error' : ''}
        />
        {errors.orcamento && <p className="error-message-inline">{errors.orcamento}</p>}
      </div>

      <div className="form-group">
        <label htmlFor="tipoViajante">Tipo de Viajante:</label>
        <select
          id="tipoViajante"
          value={tipoViajante}
          onChange={(e) => setTipoViajante(e.target.value)}
          required
          className={errors.tipoViajante ? 'input-error' : ''}
        >
          <option value="">Selecione...</option>
          <option value="aventureiro">Aventureiro</option>
          <option value="relax">Relax</option>
          <option value="cultural">Cultural</option>
          <option value="gastronomico">Gastronômico</option>
          <option value="familia">Família</option>
        </select>
        {errors.tipoViajante && <p className="error-message-inline">{errors.tipoViajante}</p>}
      </div>

      <div className="form-group">
        <label>Interesses:</label>
        <div className="checkbox-group">
          <label>
            <input
              type="checkbox"
              value="praias"
              checked={interesses.includes('praias')}
              onChange={handleInteresseChange}
            /> Praias
          </label>
          <label>
            <input
              type="checkbox"
              value="museus"
              checked={interesses.includes('museus')}
              onChange={handleInteresseChange}
            /> Museus
          </label>
          <label>
            <input
              type="checkbox"
              value="trilhas"
              checked={interesses.includes('trilhas')}
              onChange={handleInteresseChange}
            /> Trilhas
          </label>
          <label>
            <input
              type="checkbox"
              value="vida-noturna"
              checked={interesses.includes('vida-noturna')}
              onChange={handleInteresseChange}
            /> Vida Noturna
          </label>
          <label>
            <input
              type="checkbox"
              value="compras"
              checked={interesses.includes('compras')}
              onChange={handleInteresseChange}
            /> Compras
          </label>
          <label>
            <input
              type="checkbox"
              value="gastronomia"
              checked={interesses.includes('gastronomia')}
              onChange={handleInteresseChange}
            /> Gastronomia
          </label>
        </div>
      </div>

      <button type="submit" className="submit-button" disabled={loading}>
        {loading ? 'Gerando Roteiro...' : 'Gerar Roteiro'}
      </button>
    </form>
  );
});

export default TravelForm;