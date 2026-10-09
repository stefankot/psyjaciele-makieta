/* Native save-markup validation. It never saves, edits, or publishes content. */
(() => {
  const report = { total: 0, invalid: [], sources: {} };
  try {
    if (!window.wp.blocks.getBlockType('core/group')) window.wp.blockLibrary.registerCoreBlocks();
    for (const [source, content] of Object.entries(window.psyValidationSources || {})) {
      let count = 0;
      const inspect = blocks => {
        for (const block of blocks) {
          report.total++; count++;
          if (block.isValid === false) report.invalid.push({ source, block: block.name, className: block.attributes.className || '', errors: block.validationIssues || [] });
          inspect(block.innerBlocks || []);
        }
      };
      inspect(window.wp.blocks.parse(content));
      report.sources[source] = count;
    }
    if (!report.total) throw new Error('No native blocks loaded.');
  } catch (error) { report.error = error.message; }
  const output = document.createElement('output');
  output.id = 'psy-block-validation';
  output.dataset.report = JSON.stringify(report);
  output.textContent = report.error || `Gutenberg: ${report.total} bloków, ${report.invalid.length} niepoprawnych`;
  output.style.cssText = 'position:fixed;bottom:70px;left:12px;z-index:100001;background:#fff;color:#124e2c;padding:12px;font:14px/1.4 Arial,sans-serif;max-width:calc(100vw - 24px)';
  document.body.append(output);
})();
