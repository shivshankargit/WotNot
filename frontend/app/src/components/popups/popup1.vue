<template>
    <div class="popup1">
      <div class="popup1-inner">
        <span class="close" @click="$emit('close')">&times;</span>
        <slot/>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PopUp1'
  }
  </script>
  
  <style scoped>
  .popup1 {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: rgba(0, 0, 0, 0.4); /* Darkened overlay */
    display: flex;
    justify-content: center;
    align-items: center; /* Center the popup vertically */
    z-index: 10000;
  }
  
  .popup1-inner {
    background-color: #f5f6fa;
    padding: 20px;
    border-radius: 8px;
    width: 300px; /* Reduced width */
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    position: relative; /* Ensures close button is relative to this container */
  }
  
  .close {
    position: absolute;
    top: 10px; /* Positioned closer to the top-right corner */
    right: 10px;
    font-size: 20px;
    cursor: pointer;
    color: black;
  }
  </style>
  