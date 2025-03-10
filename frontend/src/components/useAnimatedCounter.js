import { ref, onMounted } from 'vue'

export function useAnimatedCounter(targetValue, duration = 2000) {
  const currentValue = ref(0)

  onMounted(() => {
    const startTime = performance.now()
    
    const updateCounter = (currentTime) => {
      const elapsed = currentTime - startTime
      const progress = Math.min(elapsed / duration, 1)
      const easeOutQuad = progress * (2 - progress)
      currentValue.value = Math.round(targetValue * easeOutQuad)
      
      if (progress < 1) {
        requestAnimationFrame(updateCounter)
      } else {
        currentValue.value = targetValue
      }
    }
    
    requestAnimationFrame(updateCounter)
  })

  return currentValue
}