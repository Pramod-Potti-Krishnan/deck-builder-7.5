/**
 * AI Regeneration Panel
 * Appears when sections are selected in review mode
 * Handles communication with backend API for section regeneration
 *
 * Part of Phase 2: World-Class Editor with AI-Powered Regeneration
 */

/**
 * Regenerate selected sections with AI
 */
async function regenerateSelectedSections() {
  const sections = getSelectedSections();

  if (sections.length === 0) {
    if (typeof showNotification === 'function') {
      showNotification('No sections selected', 'warning');
    }
    return;
  }

  const input = document.getElementById('ai-instruction-input');
  const instruction = input?.value;

  if (!instruction || instruction.trim() === '') {
    if (typeof showNotification === 'function') {
      showNotification('Please enter an instruction for the AI', 'warning');
    }
    input?.focus();
    return;
  }

  console.log(`🤖 Regenerating ${sections.length} section(s) with AI...`);

  if (typeof showNotification === 'function') {
    showNotification('🤖 Regenerating with AI...', 'info');
  }

  // Disable regenerate button during processing
  const regenerateBtn = document.getElementById('regenerate-btn');
  if (regenerateBtn) {
    regenerateBtn.disabled = true;
    regenerateBtn.textContent = 'Regenerating...';
  }

  try {
    for (const section of sections) {
      console.log(`Processing: ${section.sectionId}`);

      // Get presentation ID from global data
      const presentationId = window.PRESENTATION_DATA?.id || 'unknown';

      const response = await fetch(
        `/api/presentations/${presentationId}/regenerate-section`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            slide_index: section.slideIndex,
            section_id: section.sectionId,
            section_type: section.sectionType,
            user_instruction: instruction.trim(),
            current_content: section.content,
            layout: section.layout
          })
        }
      );

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.detail || `API error: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        // Update section in DOM
        updateSectionInDOM(section.sectionId, data.updated_content);
        console.log(`✅ Updated: ${section.sectionId}`);
      } else {
        throw new Error(data.message || 'Regeneration failed');
      }
    }

    if (typeof showNotification === 'function') {
      showNotification(
        `✅ ${sections.length} section${sections.length !== 1 ? 's' : ''} regenerated successfully!`,
        'success'
      );
    }

    clearSelection();

    // Clear instruction input
    if (input) input.value = '';

  } catch (error) {
    console.error('Regeneration error:', error);
    if (typeof showNotification === 'function') {
      showNotification(`❌ Error: ${error.message}`, 'error');
    }
  } finally {
    // Re-enable regenerate button
    if (regenerateBtn) {
      regenerateBtn.disabled = false;
      regenerateBtn.textContent = 'Regenerate with AI';
    }
  }
}

/**
 * Update section content in DOM with animation
 */
function updateSectionInDOM(sectionId, newContent) {
  const element = document.querySelector(`[data-section-id="${sectionId}"]`);
  if (!element) {
    console.warn(`Section not found: ${sectionId}`);
    return;
  }

  // Fade out animation
  element.style.transition = 'opacity 0.3s ease';
  element.style.opacity = '0.3';

  setTimeout(() => {
    // Update content
    element.innerHTML = newContent;

    // Fade in animation
    element.style.opacity = '1';

    // Highlight briefly to show change
    element.style.backgroundColor = 'rgba(16, 185, 129, 0.1)';
    setTimeout(() => {
      element.style.backgroundColor = '';
    }, 2000);
  }, 300);
}

// Export functions for global access
if (typeof window !== 'undefined') {
  window.regenerateSelectedSections = regenerateSelectedSections;
  window.updateSectionInDOM = updateSectionInDOM;
}

console.log('✅ Regeneration Panel module loaded');
