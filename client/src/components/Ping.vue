<template>
  <div class="container">
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Ping',
  data() {
    return {
      message: '',
    };
  },
  methods: {
    getMessage() {
      const path = `http://localhost:5000/ping`;
      axios.get(path)
        .then((res) => {
          this.message = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
