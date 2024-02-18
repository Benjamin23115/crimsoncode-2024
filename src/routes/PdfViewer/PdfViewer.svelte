<script lang="ts">
import PDFJSExpress from '@pdftron/pdfjs-express-viewer'

export let appTheme: "light" | "dark" = "light"; 

PDFJSExpress({
  path: 'src/pdf-js',
  licenseKey: 'YOUR_KEY_HERE',
}, document.getElementById('viewer'))
  .then(instance => {
    instance.UI.setTheme('dark');  })

</script>

<style lang="postcss">
</style>
