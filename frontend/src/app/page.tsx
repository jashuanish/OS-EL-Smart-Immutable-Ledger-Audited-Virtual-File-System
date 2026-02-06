'use client'

import { useState, useEffect } from 'react'
import FileExplorer from '@/components/FileExplorer'
import ZoneVisualization from '@/components/ZoneVisualization'
import BlockchainViewer from '@/components/BlockchainViewer'
import OSDashboard from '@/components/OSDashboard'
import FileUpload from '@/components/FileUpload'
import FaceAuthModal from '@/components/FaceAuthModal'
import LocalFileBrowser from '@/components/LocalFileBrowser'
import { FileMetadata } from '@/types'

export default function Home() {
  const [files, setFiles] = useState<FileMetadata[]>([])
  const [selectedFile, setSelectedFile] = useState<FileMetadata | null>(null)
  const [activeTab, setActiveTab] = useState<'explorer' | 'local' | 'zones' | 'blockchain' | 'kernel'>('explorer')
  const [userId, setUserId] = useState('demo_user')
  const [loading, setLoading] = useState(true)

  // Biometric Enrollment State
  const [isEnrolled, setIsEnrolled] = useState(false)
  const [showEnrollment, setShowEnrollment] = useState(false)
  // ...

  useEffect(() => {
    fetchFiles()
  }, [])

  const fetchFiles = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/files`, {
        headers: {
          'X-User-ID': userId
        }
      })
      const data = await response.json()
      setFiles(data)
    } catch (error) {
      console.error('Error fetching files:', error)
    } finally {
      setLoading(false)
    }
  }

  // Reload when userId changes
  useEffect(() => {
    fetchFiles()
  }, [userId])

  const handleFileUploaded = () => {
    fetchFiles()
  }

  const handleEnrollmentSuccess = () => {
    setIsEnrolled(true)
    setShowEnrollment(false)
    alert("Biometric Identity Registered Successfully!")
  }

  return (
    <div className="min-h-screen bg-gray-50">

      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">CryptoFS++</h1>
              <p className="text-sm text-gray-500">AI-Governed, Blockchain-Audited File System</p>
            </div>
            <div className="flex items-center space-x-4">

              {/* Enrollment Button */}
              {!isEnrolled && userId === 'demo_user' && (
                <button
                  onClick={() => setShowEnrollment(true)}
                  className="flex items-center space-x-2 px-3 py-1 bg-purple-100 text-purple-700 rounded-md hover:bg-purple-200 text-sm font-medium"
                >
                  <span>👤 Register Identity</span>
                </button>
              )}
              {isEnrolled && (
                <span className="text-xs font-bold text-green-600 bg-green-50 px-2 py-1 rounded border border-green-200">
                  verified_id: {userId}
                </span>
              )}

              {/* User Context Toggle */}
              <div className="flex items-center bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setUserId('demo_user')}
                  className={`px-3 py-1 text-sm font-medium rounded-md ${userId === 'demo_user' ? 'bg-white shadow text-blue-600' : 'text-gray-500'}`}
                >
                  Admin
                </button>
                <button
                  onClick={() => setUserId('guest_user')}
                  className={`px-3 py-1 text-sm font-medium rounded-md ${userId === 'guest_user' ? 'bg-white shadow text-blue-600' : 'text-gray-500'}`}
                >
                  Guest
                </button>
              </div>
              <FileUpload onUploaded={handleFileUploaded} />
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('explorer')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${activeTab === 'explorer'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
            >
              Vault (Simulation)
            </button>
            <button
              onClick={() => setActiveTab('local')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${activeTab === 'local'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
            >
              Local Files (Real FS)
            </button>
            <button
              onClick={() => setActiveTab('zones')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${activeTab === 'zones'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
            >
              Sensitivity Zones
            </button>
            <button
              onClick={() => setActiveTab('blockchain')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${activeTab === 'blockchain'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
            >
              Blockchain Audit
            </button>
            <button
              onClick={() => setActiveTab('kernel')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${activeTab === 'kernel'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
            >
              OS Kernel Hub
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading...</p>
          </div>
        ) : (
          <>
            {activeTab === 'explorer' && (
              <FileExplorer
                files={files}
                selectedFile={selectedFile}
                onSelectFile={setSelectedFile}
                onRefresh={fetchFiles}
                userId={userId}
                isEnrolled={isEnrolled}
              />
            )}
            {activeTab === 'local' && (
              <LocalFileBrowser
                userId={userId}
                isEnrolled={isEnrolled}
              />
            )}
            {activeTab === 'zones' && <ZoneVisualization files={files} />}
            {activeTab === 'blockchain' && <BlockchainViewer />}
            {activeTab === 'kernel' && <OSDashboard />}
          </>
        )}
      </main>

      {/* Render Modal if needed (using dynamic import or simple conditional logic if imported) */}
      {showEnrollment && (
        <FaceAuthModal
          isOpen={showEnrollment}
          onClose={() => setShowEnrollment(false)}
          onSuccess={handleEnrollmentSuccess}
          mode="enroll"
        />
      )}
    </div>
  )
}

