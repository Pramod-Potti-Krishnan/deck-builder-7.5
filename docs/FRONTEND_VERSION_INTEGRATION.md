# Frontend Version History Integration Guide

This document explains how to integrate version history functionality from the Layout Service into your frontend application via cross-origin postMessage API.

---

## Overview

The Layout Service provides version history management for presentations. Every save creates a new version, allowing users to view history and restore previous versions.

**Available Commands:**
| Command | Description |
|---------|-------------|
| `getVersionHistory` | Get list of all versions for a presentation |
| `restoreVersion` | Restore a specific version |

---

## 1. Get Version History

Fetch the complete version history for the current presentation.

### Request

```typescript
// Send command to iframe
iframeRef.contentWindow.postMessage({
  command: 'getVersionHistory',
  params: {
    presentationId: 'optional-if-already-loaded'  // Optional - uses current presentation if omitted
  }
}, '*');
```

### Response

```typescript
interface VersionHistoryResponse {
  command: 'getVersionHistory';
  success: boolean;
  presentationId: string;
  currentVersionId: string;
  versions: Array<{
    version_id: string;
    created_at: string;      // ISO 8601 timestamp
    created_by: string;      // 'user', 'auto-save', 'system', etc.
    change_summary?: string; // Optional description of changes
    presentation_id: string;
  }>;
  error?: string;  // Only present if success=false
}
```

### Example Usage

```typescript
// React/Next.js example
const [versions, setVersions] = useState([]);
const [currentVersion, setCurrentVersion] = useState('');

useEffect(() => {
  const handleMessage = (event: MessageEvent) => {
    if (event.data.command === 'getVersionHistory') {
      if (event.data.success) {
        setVersions(event.data.versions);
        setCurrentVersion(event.data.currentVersionId);
      } else {
        console.error('Failed to get versions:', event.data.error);
      }
    }
  };

  window.addEventListener('message', handleMessage);
  return () => window.removeEventListener('message', handleMessage);
}, []);

// Request versions when component mounts or user clicks "Version History"
const fetchVersionHistory = () => {
  iframeRef.current?.contentWindow?.postMessage({
    command: 'getVersionHistory'
  }, '*');
};
```

---

## 2. Restore Version

Restore the presentation to a specific previous version.

### Request

```typescript
iframeRef.contentWindow.postMessage({
  command: 'restoreVersion',
  params: {
    versionId: 'version-id-to-restore',  // Required
    presentationId: 'optional',           // Optional - uses current if omitted
    createBackup: true,                   // Optional - default true (creates backup before restore)
    reload: true                          // Optional - default true (auto-reload after restore)
  }
}, '*');
```

### Response

```typescript
interface RestoreVersionResponse {
  command: 'restoreVersion';
  success: boolean;
  message?: string;           // Success message
  backupVersionId?: string;   // ID of backup created before restore
  error?: string;             // Only present if success=false
}
```

### Example Usage

```typescript
const restoreVersion = (versionId: string) => {
  // Confirm with user
  if (!confirm('Are you sure you want to restore this version? Current changes will be backed up.')) {
    return;
  }

  iframeRef.current?.contentWindow?.postMessage({
    command: 'restoreVersion',
    params: {
      versionId: versionId,
      createBackup: true,
      reload: true
    }
  }, '*');
};

// Handle response
useEffect(() => {
  const handleMessage = (event: MessageEvent) => {
    if (event.data.command === 'restoreVersion') {
      if (event.data.success) {
        // Page will auto-reload unless reload=false was specified
        toast.success('Version restored successfully');
      } else {
        toast.error(`Restore failed: ${event.data.error}`);
      }
    }
  };

  window.addEventListener('message', handleMessage);
  return () => window.removeEventListener('message', handleMessage);
}, []);
```

---

## 3. Complete Implementation Example

### VersionHistoryPanel Component

```tsx
import React, { useState, useEffect, useRef } from 'react';

interface Version {
  version_id: string;
  created_at: string;
  created_by: string;
  change_summary?: string;
}

interface VersionHistoryPanelProps {
  iframeRef: React.RefObject<HTMLIFrameElement>;
  isOpen: boolean;
  onClose: () => void;
}

export const VersionHistoryPanel: React.FC<VersionHistoryPanelProps> = ({
  iframeRef,
  isOpen,
  onClose
}) => {
  const [versions, setVersions] = useState<Version[]>([]);
  const [currentVersionId, setCurrentVersionId] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch versions when panel opens
  useEffect(() => {
    if (isOpen) {
      fetchVersions();
    }
  }, [isOpen]);

  // Listen for postMessage responses
  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      const { command, success, error: errorMsg } = event.data;

      if (command === 'getVersionHistory') {
        setLoading(false);
        if (success) {
          setVersions(event.data.versions || []);
          setCurrentVersionId(event.data.currentVersionId);
          setError(null);
        } else {
          setError(errorMsg || 'Failed to fetch versions');
        }
      }

      if (command === 'restoreVersion') {
        if (!success) {
          setError(errorMsg || 'Failed to restore version');
        }
        // Note: Page will reload on success
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  const fetchVersions = () => {
    setLoading(true);
    setError(null);
    iframeRef.current?.contentWindow?.postMessage({
      command: 'getVersionHistory'
    }, '*');
  };

  const handleRestore = (versionId: string) => {
    if (versionId === currentVersionId) {
      alert('This is already the current version');
      return;
    }

    if (!confirm('Restore this version? Current state will be backed up.')) {
      return;
    }

    iframeRef.current?.contentWindow?.postMessage({
      command: 'restoreVersion',
      params: { versionId }
    }, '*');
  };

  const formatDate = (isoString: string) => {
    const date = new Date(isoString);
    return date.toLocaleString();
  };

  if (!isOpen) return null;

  return (
    <div className="version-history-panel">
      <div className="panel-header">
        <h3>Version History</h3>
        <button onClick={onClose}>×</button>
      </div>

      {loading && <div className="loading">Loading versions...</div>}
      {error && <div className="error">{error}</div>}

      <div className="versions-list">
        {versions.map((version) => (
          <div
            key={version.version_id}
            className={`version-item ${version.version_id === currentVersionId ? 'current' : ''}`}
          >
            <div className="version-info">
              <span className="version-date">{formatDate(version.created_at)}</span>
              <span className="version-author">{version.created_by}</span>
              {version.change_summary && (
                <span className="version-summary">{version.change_summary}</span>
              )}
            </div>
            <div className="version-actions">
              {version.version_id === currentVersionId ? (
                <span className="current-badge">Current</span>
              ) : (
                <button onClick={() => handleRestore(version.version_id)}>
                  Restore
                </button>
              )}
            </div>
          </div>
        ))}

        {versions.length === 0 && !loading && (
          <div className="empty-state">No version history available</div>
        )}
      </div>
    </div>
  );
};
```

---

## 4. Version Data Structure

Each version contains:

| Field | Type | Description |
|-------|------|-------------|
| `version_id` | string | Unique identifier for this version |
| `created_at` | string | ISO 8601 timestamp when version was created |
| `created_by` | string | Who created the version (`user`, `auto-save`, `system`, etc.) |
| `change_summary` | string? | Optional description of what changed |
| `presentation_id` | string | ID of the presentation this version belongs to |

---

## 5. Best Practices

1. **Confirm Before Restore**: Always show a confirmation dialog before restoring to prevent accidental data loss.

2. **Show Current Version**: Clearly indicate which version is currently active.

3. **Backup on Restore**: Keep `createBackup: true` (default) to allow users to undo a restore.

4. **Handle Reload**: The page reloads after restore by default. If you need to handle this differently, set `reload: false` and manually reload or update the UI.

5. **Error Handling**: Always handle the error case in your message listener.

6. **Loading States**: Show loading indicators while fetching versions or restoring.

---

## 6. Related Commands

These commands are also available via postMessage:

| Command | Description |
|---------|-------------|
| `enterEditMode` | Enter edit mode |
| `exitEditMode` | Exit edit mode |
| `forceSave` | Trigger immediate save |
| `cancelEdits` | Cancel pending edits |

---

## Questions?

If you encounter issues with cross-origin communication, ensure:
1. The iframe origin is in the allowed origins list
2. You're using the correct postMessage format
3. Check browser console for any CORS-related errors
