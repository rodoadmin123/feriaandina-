// Fichas de categoria que se deslizan con el pulgar.
export default function FiltroCategorias({ categorias, activa, onElegir }) {
  return (
    <div className="chips" role="tablist" aria-label="Categorías">
      <button className={`chip ${!activa ? "activa" : ""}`} onClick={() => onElegir(null)}>
        Todo
      </button>
      {categorias.map((c) => (
        <button key={c.id} className={`chip ${activa === c.id ? "activa" : ""}`}
          onClick={() => onElegir(c.id)}>
          {c.nombre}
        </button>
      ))}
    </div>
  );
}
