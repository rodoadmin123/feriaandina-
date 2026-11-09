import { createContext, useContext, useMemo, useState } from "react";

// CONTEXTO PEDIDOS: el carrito vive en el navegador hasta que se paga.
// React Context permite que cualquier pantalla lo use (detalle, barra, carrito).
const Contexto = createContext(null);

export function CarritoProveedor({ children }) {
  const [items, setItems] = useState([]); // [{producto, cantidad}]

  const agregar = (producto, cantidad) => {
    setItems((actual) => {
      const existe = actual.find((i) => i.producto.id === producto.id);
      if (existe) {
        return actual.map((i) => i.producto.id === producto.id
          ? { ...i, cantidad: Math.min(producto.stock, i.cantidad + cantidad) } : i);
      }
      return [...actual, { producto, cantidad }];
    });
  };
  const cambiarCantidad = (id, cantidad) =>
    setItems((a) => a.map((i) => (i.producto.id === id ? { ...i, cantidad } : i)));
  const quitar = (id) => setItems((a) => a.filter((i) => i.producto.id !== id));
  const vaciar = () => setItems([]);

  const valor = useMemo(() => ({
    items, agregar, cambiarCantidad, quitar, vaciar,
    cantidadTotal: items.reduce((s, i) => s + i.cantidad, 0),
    total: items.reduce((s, i) => s + i.cantidad * Number(i.producto.precio), 0),
  }), [items]);

  return <Contexto.Provider value={valor}>{children}</Contexto.Provider>;
}

export const useCarrito = () => useContext(Contexto);
