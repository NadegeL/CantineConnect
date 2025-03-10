import { defineConfig } from 'unocss'
import { presetUno, presetIcons } from 'unocss'

export default defineConfig({
    presets: [
        presetUno(),
        presetIcons({
            collections: {
                carbon: () => import('@iconify-json/carbon/icon.json').then(i => i.default),
                mdi: () => import('@iconify-json/mdi/icon.json').then(i => i.default),
            }
        })
    ]
})
