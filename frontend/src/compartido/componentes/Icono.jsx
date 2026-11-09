// Iconos simples en SVG (no se necesita ninguna libreria extra).
const trazos = {
  tienda: "M3 9l1.5-5h15L21 9M4 9h16v11H4zM9 20v-6h6v6",
  camara: "M4 8h3l2-3h6l2 3h3v11H4zM12 17a4 4 0 100-8 4 4 0 000 8z",
  carrito: "M3 4h2l2.4 11h10.2L20 7H6.2M9 20a1 1 0 100-2 1 1 0 000 2zM17 20a1 1 0 100-2 1 1 0 000 2z",
  atras: "M15 5l-7 7 7 7",
  buscar: "M11 18a7 7 0 100-14 7 7 0 000 14zM20 20l-4-4",
  ubicacion: "M12 21s7-6.2 7-11.5A7 7 0 005 9.5C5 14.8 12 21 12 21zM12 12a2.5 2.5 0 100-5 2.5 2.5 0 000 5z",
  check: "M5 12.5l4.5 4.5L19 7",
  basura: "M5 7h14M10 7V4h4v3M7 7l1 13h8l1-13",
};
export default function Icono({ nombre, tam = 24 }) {
  return (
    <svg width={tam} height={tam} viewBox="0 0 24 24" fill="none" stroke="currentColor"
      strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d={trazos[nombre]} />
    </svg>
  );
}
