import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { soles } from "../../../compartido/api.js";
import Contador from "../../../compartido/componentes/Contador.jsx";
import Icono from "../../../compartido/componentes/Icono.jsx";
import { listarCategorias, publicarProducto } from "../../catalogo/api.js";
import { listarArtesanos } from "../api.js";
import SelectorFoto from "../componentes/SelectorFoto.jsx";

// PANTALLA 3 - VENDER (IDL1, paso 3: el productor publica su producto)
// Pensada para el reto de Andrea: "con el celular, con una sola mano y
// sin manual": 1 foto + 4 datos, botones grandes y el boton principal
// abajo, donde llega el pulgar.
export default function PublicarProducto() {
  const [artesanos, setArtesanos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [form, setForm] = useState({ artesano_id: "", nombre: "", precio: "", categoria: "" });
  const [stock, setStock] = useState(1);
  const [foto, setFoto] = useState(null);
  const [enviando, setEnviando] = useState(false);
  const [error, setError] = useState("");
  const [publicado, setPublicado] = useState(null);

  useEffect(() => {
    listarArtesanos().then((lista) => {
      setArtesanos(lista);
      if (lista.length) setForm((f) => ({ ...f, artesano_id: String(lista[0].id) }));
    });
    listarCategorias().then(setCategorias);
  }, []);

  const cambiar = (campo) => (e) => setForm({ ...form, [campo]: e.target.value });

  const enviar = async (e) => {
    e.preventDefault();
    setError("");
    // FormData: empaqueta texto + foto para enviarlos a Django
    const datos = new FormData();
    Object.entries(form).forEach(([k, v]) => datos.append(k, v));
    datos.append("stock", stock);
    if (foto) datos.append("foto", foto);
    setEnviando(true);
    try {
      setPublicado(await publicarProducto(datos));
    } catch (err) {
      setError(err.message);   // mensaje de la regla de dominio del back-end
    } finally {
      setEnviando(false);
    }
  };

  const reiniciar = () => {
    setPublicado(null); setFoto(null); setStock(1);
    setForm({ ...form, nombre: "", precio: "", categoria: "" });
  };

  if (publicado) {
    return (
      <main className="pantalla pantalla-centrada">
        <div className="exito">
          <span className="exito-icono"><Icono nombre="check" tam={40} /></span>
          <h1>¡Producto publicado!</h1>
          <img src={publicado.foto_url} alt={publicado.nombre} />
          <p><strong>{publicado.nombre}</strong><br />{soles(publicado.precio)} · {publicado.stock} en stock</p>
          <p className="nota">Ya aparece en el catálogo. Te avisaremos por WhatsApp cuando alguien lo compre.</p>
          <Link className="boton-principal" to={`/producto/${publicado.id}`}>Ver en el catálogo</Link>
          <button className="boton-secundario" onClick={reiniciar}>Publicar otro producto</button>
        </div>
      </main>
    );
  }

  return (
    <main className="pantalla pantalla-con-accion">
      <header className="cabecera cabecera-simple">
        <h1>Vender un producto</h1>
        <label className="vendo-como">
          Vendo como
          <select value={form.artesano_id} onChange={cambiar("artesano_id")}>
            {artesanos.map((a) => (
              <option key={a.id} value={a.id}>{a.nombre} · {a.comunidad}</option>
            ))}
          </select>
        </label>
      </header>

      <form id="form-vender" className="formulario" onSubmit={enviar}>
        <SelectorFoto foto={foto} onElegir={setFoto} />

        <label className="campo">
          <span>¿Qué vendes?</span>
          <input value={form.nombre} onChange={cambiar("nombre")} placeholder="Ej. Chullo de lana" />
        </label>

        <fieldset className="campo">
          <legend>Categoría</legend>
          <div className="chips chips-envolver">
            {categorias.map((c) => (
              <button type="button" key={c.id}
                className={`chip ${form.categoria === c.id ? "activa" : ""}`}
                onClick={() => setForm({ ...form, categoria: c.id })}>
                {c.nombre}
              </button>
            ))}
          </div>
        </fieldset>

        <div className="fila-doble">
          <label className="campo">
            <span>Precio</span>
            <div className="entrada-precio">
              <b>S/</b>
              {/* inputMode="decimal" abre el teclado NUMERICO del celular */}
              <input inputMode="decimal" value={form.precio} onChange={cambiar("precio")} placeholder="0.00" />
            </div>
          </label>
          <div className="campo">
            <span>¿Cuántos tienes?</span>
            <Contador valor={stock} onCambiar={setStock} minimo={1} etiqueta="Stock" />
          </div>
        </div>

        {error && <p className="aviso aviso-error" role="alert">{error}</p>}
      </form>

      <div className="accion-fija">
        <button className="boton-principal" type="submit" form="form-vender" disabled={enviando}>
          {enviando ? "Publicando…" : "Publicar producto"}
        </button>
      </div>
    </main>
  );
}
