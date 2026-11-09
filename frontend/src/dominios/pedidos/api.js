// CONTEXTO PEDIDOS
import { pedirApi } from "../../compartido/api.js";

export const realizarPedido = (pedido) =>
  pedirApi("/pedidos/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(pedido),
  });
