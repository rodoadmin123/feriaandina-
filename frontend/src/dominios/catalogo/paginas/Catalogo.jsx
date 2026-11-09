import { useEffect, useState } from "react";
import Icono from "../../../compartido/componentes/Icono.jsx";
import { listarCategorias, listarProductos } from "../api.js";
import FiltroCategorias from "../componentes/FiltroCategorias.jsx";
import TarjetaProducto from "../componentes/TarjetaProducto.jsx";

// PANTALLA 1 - CATALOGO (IDL1, paso 5: el comprador busca y filtra)
export default function Catalogo() {
  const [productos, setProductos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [categoria, setCategoria] = useState(null);
  const [texto, setTexto] = useState("");
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  // Se ejecuta al abrir la pantalla: trae las categorias del back-end
  useEffect(() => {
    listarCategorias().then(setCategorias).catch(() => {});
  }, []);

  // Se ejecuta cada vez que cambia la categoria o el texto buscado
  useEffect(() => {
    setCargando(true);
    const espera = setTimeout(() => {
      listarProductos({ categoria, texto })
        .then((datos) => { setProductos(datos); setError(""); })
        .catch((e) => setError(e.message))
        .finally(() => setCargando(false));
    }, 250); // pequena espera para no llamar a la API en cada letra
    return () => clearTimeout(espera);
  }, [categoria, texto]);

  return (
    <main className="pantalla">
      <header className="cabecera">
        <div className="marca">
          <img src="/icono.svg" alt="" width="36" height="36" />
          <div>
            <h1>FeriaAndina</h1>
            <p>Hecho a mano en el Valle del Mantaro</p>
          </div>
        </div>
        <label className="buscador">
          <Icono nombre="buscar" tam={20} />
          <input type="search" placeholder="Busca mantas, café, mates…"
            value={texto} onChange={(e) => setTexto(e.target.value)} />
        </label>
      </header>

      <FiltroCategorias categorias={categorias} activa={categoria} onElegir={setCategoria} />

      {error && <p className="aviso aviso-error">{error}</p>}
      {!cargando && !error && productos.length === 0 && (
        <p className="vacio">No encontramos productos. Prueba otra búsqueda.</p>
      )}
      <section className="rejilla" aria-busy={cargando}>
        {productos.map((p) => <TarjetaProducto key={p.id} producto={p} />)}
      </section>
    </main>
  );
}
