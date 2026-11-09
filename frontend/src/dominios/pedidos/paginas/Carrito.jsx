import { useState } from "react";
import { Link } from "react-router-dom";
import { soles } from "../../../compartido/api.js";
import Contador from "../../../compartido/componentes/Contador.jsx";
import Icono from "../../../compartido/componentes/Icono.jsx";
import { realizarPedido } from "../api.js";
import { useCarrito } from "../CarritoContexto.jsx";

// PANTALLA 4 - CARRITO Y PAGO (IDL1, pasos 6 y 7)
export default function Carrito() {
  const { items, cambiarCantidad, quitar, vaciar, total } = useCarrito();
  const [comprador, setComprador] = useState("");
  const [telefono, setTelefono] = useState("");
  const [metodo, setMetodo] = useState("yape");
  const [error, setError] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [pedido, setPedido] = useState(null);

  const pagar = async () => {
    setError(""); setEnviando(true);
    try {
      const resultado = await realizarPedido({
        comprador, telefono, metodo_pago: metodo,
        items: items.map((i) => ({ producto_id: i.producto.id, cantidad: i.cantidad })),
      });
      setPedido(resultado);
      vaciar();
    } catch (e) {
      setError(e.message);
    } finally {
      setEnviando(false);
    }
  };

  if (pedido) {
    return (
      <main className="pantalla pantalla-centrada">
        <div className="exito">
          <span className="exito-icono"><Icono nombre="check" tam={40} /></span>
          <h1>¡Pago aprobado!</h1>
          <p>Pedido <strong>N.° {String(pedido.id).padStart(5, "0")}</strong> · estado <span className="estado">{pedido.estado}</span></p>
          <ul className="resumen">
            {pedido.lineas.map((l) => (
              <li key={l.nombre}><span>{l.cantidad} × {l.nombre}</span><b>{soles(l.subtotal)}</b></li>
            ))}
            <li className="resumen-total"><span>Total pagado</span><b>{soles(pedido.total)}</b></li>
          </ul>
          <p className="nota">Código de operación: {pedido.codigo_pago}<br />El artesano ya recibió el aviso para preparar tu envío.</p>
          <Link className="boton-principal" to="/">Seguir comprando</Link>
        </div>
      </main>
    );
  }

  if (items.length === 0) {
    return (
      <main className="pantalla pantalla-centrada">
        <div className="exito">
          <span className="exito-icono gris"><Icono nombre="carrito" tam={36} /></span>
          <h1>Tu carrito está vacío</h1>
          <Link className="boton-principal" to="/">Ver productos</Link>
        </div>
      </main>
    );
  }

  return (
    <main className="pantalla pantalla-con-accion">
      <header className="cabecera cabecera-simple"><h1>Tu carrito</h1></header>
      <ul className="lista-carrito">
        {items.map(({ producto, cantidad }) => (
          <li key={producto.id}>
            <img src={producto.foto_url} alt="" />
            <div className="linea-info">
              <strong>{producto.nombre}</strong>
              <span>{producto.artesano.comunidad} · {soles(producto.precio)}</span>
              <div className="linea-acciones">
                <Contador valor={cantidad} maximo={producto.stock} etiqueta="Cantidad"
                  onCambiar={(c) => cambiarCantidad(producto.id, c)} />
                <button className="boton-icono" onClick={() => quitar(producto.id)} aria-label="Quitar">
                  <Icono nombre="basura" tam={20} />
                </button>
              </div>
            </div>
          </li>
        ))}
      </ul>

      <section className="formulario">
        <label className="campo"><span>Tu nombre</span>
          <input value={comprador} onChange={(e) => setComprador(e.target.value)} placeholder="Nombre y apellido" />
        </label>
        <label className="campo"><span>Celular</span>
          <input inputMode="tel" value={telefono} onChange={(e) => setTelefono(e.target.value)} placeholder="9XX XXX XXX" />
        </label>
        <fieldset className="campo">
          <legend>¿Cómo pagas?</legend>
          <div className="metodos">
            {[["yape", "Yape"], ["tarjeta", "Tarjeta"]].map(([id, nombre]) => (
              <button type="button" key={id} className={`metodo ${metodo === id ? "activa" : ""}`}
                onClick={() => setMetodo(id)}>{nombre}</button>
            ))}
          </div>
        </fieldset>
        {error && <p className="aviso aviso-error" role="alert">{error}</p>}
      </section>

      <div className="accion-fija">
        <button className="boton-principal" onClick={pagar} disabled={enviando}>
          {enviando ? "Procesando…" : `Pagar ${soles(total)}`}
        </button>
      </div>
    </main>
  );
}
