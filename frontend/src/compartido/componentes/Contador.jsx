// Contador grande (- 1 +) reutilizable: stock al vender y cantidad al comprar.
export default function Contador({ valor, onCambiar, minimo = 1, maximo = 999, etiqueta }) {
  return (
    <div className="contador" role="group" aria-label={etiqueta}>
      <button type="button" onClick={() => onCambiar(Math.max(minimo, valor - 1))}
        disabled={valor <= minimo} aria-label="Restar">−</button>
      <output>{valor}</output>
      <button type="button" onClick={() => onCambiar(Math.min(maximo, valor + 1))}
        disabled={valor >= maximo} aria-label="Sumar">+</button>
    </div>
  );
}
