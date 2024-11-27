<template>
    <div class="fixed inset-0 bg-black bg-opacity-20 flex justify-center items-center p-3 z-[10000] text-left shadow-lg">
      <div class="bg-[#ffffff] p-6 rounded-md w-[400px] overflow-y-hidden relative max-h-[750px]">
        <div class="flex justify-end">
            <span class="close" @click="$emit('close')" hover>&times;</span> 
        </div>
          
        <slot/>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PopUp_preview'
  }
  </script>
  
  <style scoped>
.close{

  padding-left: 200px;
  font-size: 25px;
  cursor: pointer;
}
</style>