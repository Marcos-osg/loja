<template>
  <v-row>
    <v-col v-for="produto in produtos" :key="produto" cols="12" sm="3">
      <v-card class="mx-auto my-12" max-width="300">
        <v-img height="220" src="https://cdn.vuetifyjs.com/images/cards/cooking.png" cover></v-img>

        <v-card-item>
          <v-card-title>{{produto.tipo}} {{ produto.marca }}</v-card-title>
          <v-card-subtitle>
            <span class="me-1">{{ produto.cor }} {{ produto.tamanho }}</span>
            <v-icon color="error" icon="mdi-fire-circle" size="small"></v-icon>
          </v-card-subtitle>
        </v-card-item>

        <v-card-text>
          <v-row align="center" class="mx-0">
          </v-row>
          <div class="my-4 text-subtitle-1" v-if="produto.preco_promo">
            <div class="my-4 text-subtitle-1">
              De: R$ {{ produto.preco }}  Por: R$ {{ produto.preco_promo }}
            </div>
          </div>
          <div class="my-4 text-subtitle-1" v-else>R$ {{ produto.preco }}</div>
          <div>
            <p>
              {{produto.tipo}} {{produto.marca}}
            </p>
            <p>
              Cor: {{produto.cor}}  Tamanho: {{produto.tamanho}}
            </p>
          </div>
        </v-card-text>

        <v-divider class="mx-4 mb-1"></v-divider>
        <v-card-actions>
          <v-btn color="deep-purple-lighten-2" variant="text" @click="addToCart(produto.id)">
            Adicionar ao Carrinho
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped>
</style>

<script setup>
import axios from "axios";
import { ref } from "vue";

const urlProdutos = "http://127.0.0.1:8000/loja/v1/todos-os-produtos";
const urlAddToCart = "http://127.0.0.1:8000/loja/v1/adiciona-item-carrinho"
const produtos = ref();

async function getProducts() {
  axios
    .get(urlProdutos)
    .then(function (response) {
      console.log(response.data);
      produtos.value = response.data;
    })
    .catch(function (error) {
      console.log("Erro");
      console.log(error);
    });
}
getProducts();

async function addToCart(id){
  axios.post(urlAddToCart, {
    "id_produto": id,
    "quantidade": 1
  }).then(function (response) {
    console.log(response.data);
  })
  .catch(function (error) {
    console.error(error);
  })
}
</script>