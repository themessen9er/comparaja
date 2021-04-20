<template>
  <div id="app">
    <h1>Broadband products</h1>
    <div
        class="product "
        :class="{ 'sponsored' : product.is_sponsored }"
        v-for="product in products"
        :key="product.id"
      >
      <div class="product-avatar">
        <h6>offer by</h6>
        <img :src="product.provider_logo_url" />
      </div>
      <div class="product-details">
        <h2 class="product-name">
          {{ product.provider_name }}
        </h2>
        <ul>
          <li><strong>Internet Speed:</strong> {{ product.internet_download_speed_in_mbs }}Mbps</li>
          <li><strong>TV Channels:</strong> {{ product.tv_channels }}</li>
          <li><strong>Mobile Data:</strong> {{ product.mobile_phone_data_in_gbps }}Gbps</li>          
          <li><strong>Mobile Phones:</strong> {{ product.mobile_phone_count }}</li>
        </ul>
      </div>
      <div class="actions-wrapper">
        <div class="price">Only {{ product.price }}€</div>
        <button class="btn">Subscribe</button>
      </div>
    </div>
  </div>
</template>

<script>

import axios from "axios";

export default {
  data() {
    return {
      products: [],
      currentPage: 0,
      numPages: 0
    };
  },
  methods: {
    getFirstPage() {
      var vm = this;
      vm.currentPage = 0;
      axios.get(process.env.VUE_APP_API_BASE_URI + '/products', { params: { page_number: vm.currentPage + 1 } }).then((response) => {
        vm.products = response.data;
        vm.currentPage = parseInt(response.headers['x-page-number']);
        vm.numPages = parseInt(response.headers['x-num-pages']);
      });
    },
    getNextPage() {
      var vm = this;
      window.onscroll = () => {
        let bottomOfWindow = Math.ceil(document.documentElement.scrollTop + window.innerHeight) >= document.documentElement.offsetHeight;
        if (bottomOfWindow && vm.currentPage < vm.numPages) { 
          axios.get(process.env.VUE_APP_API_BASE_URI + '/products', { params: { page_number: 1 + vm.currentPage } }).then(response => {
            vm.products = vm.products.concat(response.data);
            vm.currentPage = parseInt(response.headers['x-page-number']);
            vm.numPages = parseInt(response.headers['x-num-pages']);
          });
        }
      }
    }
  },
  beforeMount() {
    this.getFirstPage();
  },
  mounted() {
    this.getNextPage();
  }
};
</script>

<style>

@import url('https://fonts.googleapis.com/css?family=Muli&display=swap');

* {
	box-sizing: border-box;
}

.sponsored {
  font-family: 'Muli', sans-serif;
}

.product {
  display: flex;
  margin: 1em auto;
  border: 1px solid black;
  height: 150px;
}

.product.sponsored {
  background-color: #e16b21;
	border-radius: 10px;
  border: 1px solid rgb(235, 235, 235);
	box-shadow: 0 10px 10px rgba(0, 0, 0, 0.2);
	display: flex;
	max-width: 100%;
	overflow: hidden;
}

.product h6 {
	opacity: 0.6;
	margin: 0;
	letter-spacing: 1px;
	text-transform: uppercase;
}

.product ul {
    margin-top: 3em;

}

.product-avatar {
  padding: 1em;
}

.product-avatar img {
  display: block;
  width: 100%;
  min-width: 64px;
  margin-top: 5px;
  height: auto;
}

.product.sponsored .product-avatar {
  background-color: #fff;
	color: rgb(80, 80, 80);
	padding: 30px;
	max-width: 250px;
}

.product-details {
  padding: 1em;
}

.product.sponsored .product-details {
	color: #fff;
	padding: 10px 30px 10px 30px;
  display: flex;
  width: 100%;
  min-width: 150px;
  height: 0em;
}

.product.sponsored .product-details ul{
  font-size: 15px;
  list-style-type: none;
  padding-inline-start: 0px;
}

.product-name {
  margin: 0;
  padding: 0;
  font-size: 2rem;
  font-weight: 900;
  position: absolute;
}

.product.sponsored .actions-wrapper {
  position: relative;
  display: flex;
  width: 15em;
  right: 20px;
}

.product.sponsored .price {
  height: 2.5em;
  position: absolute;
  top: 15px;
  right: -20px;
  width: 180px;
  background-color: antiquewhite;
  box-shadow: 0 3px 3px rgba(0, 0, 0, 0.3);
  padding: 10px 10px 10px 30px;
  font-size: 1.1em;
  font-weight: bold;
}

.product.sponsored .btn {
	background-color: white;
	border: 0;
	border-radius: 50px;
	box-shadow: 0 10px 10px rgba(0, 0, 0, 0.2);
	color: rgb(85, 85, 85);
	font-size: 16px;
	padding: 12px 25px;
	position: absolute;
	bottom: 30px;
	right: 10px;
	letter-spacing: 1px;
}

</style>
