'use client'

import { useState, useEffect } from 'react'
import { Folder, File, ChevronRight, ChevronDown, Home, Lock, Unlock, Trash2, Edit2, Plus, RefreshCw, AlertCircle } from 'lucide-react'
import FaceAuthModal from './FaceAuthModal'

interface LocalFile {
    name: string
    path: string
    size: number
    modified: string
    extension?: string
    is_encrypted: boolean
}

interface LocalFolder {
    name: string
    path: string
    modified: string
}

interface DirectoryContents {
    path: string
    files: LocalFile[]
    folders: LocalFolder[]
    parent: string | null
}

interface LocalFileBrowserProps {
    userId: string
    isEnrolled: boolean
}

export default function LocalFileBrowser({ userId, isEnrolled }: LocalFileBrowserProps) {
    const [roots, setRoots] = useState<any[]>([])
    const [currentPath, setCurrentPath] = useState<string>('')
    const [contents, setContents] = useState<DirectoryContents | null>(null)
    const [loading, setLoading] = useState(false)
    const [selectedItem, setSelectedItem] = useState<string | null>(null)
    const [showFaceAuth, setShowFaceAuth] = useState(false)
    const [pendingOperation, setPendingOperation] = useState<{ type: string, path: string } | null>(null)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        fetchRoots()
    }, [])

    const fetchRoots = async () => {
        try {
            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/local/roots`,
                {
                    headers: { 'X-User-ID': userId }
                }
            )
            const data = await response.json()
            setRoots(data.roots)

            // Auto-select first existing root
            const firstRoot = data.roots.find((r: any) => r.exists)
            if (firstRoot && !currentPath) {
                browseDirectory(firstRoot.path)
            }
        } catch (error) {
            console.error('Error fetching roots:', error)
            setError('Failed to fetch filesystem roots')
        }
    }

    const browseDirectory = async (path: string) => {
        setLoading(true)
        setError(null)
        try {
            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/local/browse?path=${encodeURIComponent(path)}`,
                {
                    headers: { 'X-User-ID': userId }
                }
            )

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Generic Server Error' }))
                throw new Error(errorData.detail || 'Failed to browse directory')
            }

            const data = await response.json()
            setContents(data)
            setCurrentPath(path)
        } catch (err: any) {
            console.error('Error browsing directory:', err)
            setError(err.message)
            alert(`Error: ${err.message}`)
        } finally {
            setLoading(false)
        }
    }

    const handleEncrypt = (path: string) => {
        if (!isEnrolled) {
            alert('⚠️ Biometric Identity Not Registered!\n\nPlease register your identity first.')
            return
        }
        setPendingOperation({ type: 'encrypt', path })
        setShowFaceAuth(true)
    }

    const handleDecrypt = (path: string) => {
        if (!isEnrolled) {
            alert('⚠️ Biometric Identity Not Registered!\n\nPlease register your identity first.')
            return
        }
        setPendingOperation({ type: 'decrypt', path })
        setShowFaceAuth(true)
    }

    const performOperation = async () => {
        if (!pendingOperation) return

        const { type, path } = pendingOperation
        setPendingOperation(null)
        setShowFaceAuth(false)

        try {
            const endpoint = type === 'encrypt' ? 'encrypt' : 'decrypt'
            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/local/${endpoint}?path=${encodeURIComponent(path)}`,
                {
                    method: 'POST',
                    headers: { 'X-User-ID': userId }
                }
            )

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Operation failed' }))
                throw new Error(errorData.detail || `${type} failed`)
            }

            const result = await response.json()
            alert(result.message)

            // Refresh directory
            if (currentPath) {
                browseDirectory(currentPath)
            }
        } catch (err: any) {
            console.error(`${type} error:`, err)
            alert(`Failed: ${err.message}`)
        }
    }

    const handleDelete = async (path: string) => {
        if (!confirm(`Are you sure you want to delete: ${path.split('\\').pop()}?`)) {
            return
        }

        try {
            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/local/file?path=${encodeURIComponent(path)}`,
                {
                    method: 'DELETE',
                    headers: { 'X-User-ID': userId }
                }
            )

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Delete failed' }))
                throw new Error(errorData.detail || 'Delete failed')
            }

            const result = await response.json()
            alert(result.message)

            // Refresh directory
            if (currentPath) {
                browseDirectory(currentPath)
            }
        } catch (err: any) {
            console.error('Delete error:', err)
            alert(`Error: ${err.message}`)
        }
    }

    const formatFileSize = (bytes: number): string => {
        if (bytes < 1024) return `${bytes} B`
        if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
        return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
    }

    const formatDate = (isoDate: string): string => {
        return new Date(isoDate).toLocaleString()
    }

    return (
        <div className="space-y-6">

            {/* Face Auth Modal */}
            <FaceAuthModal
                isOpen={showFaceAuth}
                onClose={() => {
                    setShowFaceAuth(false)
                    setPendingOperation(null)
                }}
                onSuccess={performOperation}
                mode="verify"
            />

            {/* Error Display */}
            {error && (
                <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded shadow-sm flex items-start space-x-3">
                    <AlertCircle className="h-5 w-5 text-red-400 mt-0.5" />
                    <div>
                        <p className="text-sm text-red-700 font-medium">Access Error</p>
                        <p className="text-xs text-red-600 mt-1">{error}</p>
                    </div>
                </div>
            )}

            {/* Header */}
            <div className="bg-white rounded-lg shadow p-4">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-bold text-gray-900">Local File System</h2>
                    <button
                        onClick={() => currentPath && browseDirectory(currentPath)}
                        className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                        title="Refresh"
                    >
                        <RefreshCw className="h-5 w-5" />
                    </button>
                </div>

                {/* Quick Access Roots */}
                <div className="flex flex-wrap gap-2">
                    {roots.filter(r => r.exists).map((root) => (
                        <button
                            key={root.path}
                            onClick={() => browseDirectory(root.path)}
                            className={`flex items-center space-x-2 px-3 py-2 rounded-lg border transition-all ${currentPath === root.path
                                ? 'bg-blue-600 border-blue-600 text-white shadow-md'
                                : 'bg-gray-50 border-gray-200 text-gray-700 hover:bg-gray-100'
                                }`}
                        >
                            <Home className="h-4 w-4" />
                            <span className="text-sm font-medium">{root.name}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* Breadcrumb */}
            {currentPath && (
                <div className="bg-white rounded-lg shadow p-3">
                    <div className="flex items-center space-x-2 text-sm">
                        <span className="text-gray-400">Location:</span>
                        <span className="font-mono text-gray-700 bg-gray-50 px-2 py-0.5 rounded border border-gray-200 truncate max-w-md" title={currentPath}>
                            {currentPath}
                        </span>
                        {contents?.parent && (
                            <button
                                onClick={() => browseDirectory(contents.parent!)}
                                className="ml-4 px-2 py-1 bg-gray-100 rounded text-blue-600 hover:bg-blue-600 hover:text-white transition-colors text-xs font-bold"
                            >
                                ↑ GO UP
                            </button>
                        )}
                    </div>
                </div>
            )}

            {/* File List */}
            {loading ? (
                <div className="bg-white rounded-lg shadow p-8 text-center">
                    <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                    <p className="mt-4 text-gray-600">Scanning directory...</p>
                </div>
            ) : contents ? (
                <div className="bg-white rounded-lg shadow overflow-hidden">
                    <div className="divide-y divide-gray-100">
                        {/* Folders */}
                        {contents.folders.map((folder) => (
                            <div
                                key={folder.path}
                                className="p-4 hover:bg-blue-50 cursor-pointer transition-all flex items-center justify-between group"
                                onClick={() => browseDirectory(folder.path)}
                            >
                                <div className="flex items-center space-x-4">
                                    <div className="bg-blue-100 p-2 rounded-lg group-hover:bg-blue-200">
                                        <Folder className="h-5 w-5 text-blue-600" />
                                    </div>
                                    <div>
                                        <p className="font-medium text-gray-900">{folder.name}</p>
                                        <p className="text-xs text-gray-500">{formatDate(folder.modified)}</p>
                                    </div>
                                </div>
                                <ChevronRight className="h-5 w-5 text-gray-300 group-hover:text-blue-400 group-hover:translate-x-1 transition-all" />
                            </div>
                        ))}

                        {/* Files */}
                        {contents.files.map((file) => (
                            <div
                                key={file.path}
                                className={`p-4 hover:bg-gray-50 transition-all flex items-center justify-between border-l-4 ${file.is_encrypted ? 'border-red-400 bg-red-50/10' : 'border-transparent'}`}
                                onClick={() => setSelectedItem(file.path)}
                            >
                                <div className="flex items-center space-x-4 flex-1 min-w-0">
                                    <div className={`p-2 rounded-lg ${file.is_encrypted ? 'bg-red-100' : 'bg-gray-100'}`}>
                                        <File className={`h-5 w-5 ${file.is_encrypted ? 'text-red-600' : 'text-gray-500'}`} />
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <p className="font-medium text-gray-900 truncate">{file.name}</p>
                                        <div className="flex items-center space-x-4 text-xs text-gray-500">
                                            <span>{formatFileSize(file.size)}</span>
                                            <span>{formatDate(file.modified)}</span>
                                            {file.is_encrypted && (
                                                <span className="inline-flex items-center px-1.5 py-0.5 rounded-full bg-red-100 text-red-700 font-bold text-[10px]">
                                                    <Lock className="h-2.5 w-2.5 mr-0.5" />
                                                    SAFE_VAULT
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                </div>

                                {/* Action Buttons */}
                                <div className="flex items-center space-x-2 ml-4">
                                    {file.is_encrypted ? (
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation()
                                                handleDecrypt(file.path)
                                            }}
                                            className="p-2 text-green-600 hover:bg-green-100 rounded-lg transition-colors"
                                            title="Decrypt with Face Auth"
                                        >
                                            <Unlock className="h-4 w-4" />
                                        </button>
                                    ) : (
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation()
                                                handleEncrypt(file.path)
                                            }}
                                            className="p-2 text-blue-600 hover:bg-blue-100 rounded-lg transition-colors"
                                            title="Encrypt with Face Auth"
                                        >
                                            <Lock className="h-4 w-4" />
                                        </button>
                                    )}
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation()
                                            handleDelete(file.path)
                                        }}
                                        className="p-2 text-red-600 hover:bg-red-100 rounded-lg transition-colors"
                                        title="Delete Permanently"
                                    >
                                        <Trash2 className="h-4 w-4" />
                                    </button>
                                </div>
                            </div>
                        ))}

                        {contents.folders.length === 0 && contents.files.length === 0 && (
                            <div className="p-12 text-center text-gray-500 bg-gray-50/50">
                                <Folder className="mx-auto h-12 w-12 text-gray-200 mb-4" />
                                <p className="font-medium">Empty Folder</p>
                                <p className="text-xs">This directory contains no accessible items.</p>
                            </div>
                        )}
                    </div>
                </div>
            ) : (
                <div className="bg-white rounded-lg shadow p-12 text-center text-gray-500">
                    <Home className="mx-auto h-16 w-16 text-gray-100 mb-4" />
                    <p className="text-lg font-medium text-gray-400">Filesystem Explorer</p>
                    <p className="text-sm">Select a root directory above to start browsing</p>
                </div>
            )}
        </div>
    )
}
