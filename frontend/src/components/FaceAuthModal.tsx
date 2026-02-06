'use client'

import React, { useState, useEffect, useRef } from 'react'
import { Scan, ShieldCheck, ShieldAlert, Camera, AlertCircle } from 'lucide-react'
import Webcam from 'react-webcam'

interface FaceAuthModalProps {
    isOpen: boolean
    onClose: () => void
    onSuccess: () => void
    mode?: 'verify' | 'enroll'
}

export default function FaceAuthModal({ isOpen, onClose, onSuccess, mode = 'verify' }: FaceAuthModalProps) {
    const [step, setStep] = useState<'init' | 'scanning' | 'success' | 'failure'>('init')
    const [progress, setProgress] = useState(0)
    const [cameraError, setCameraError] = useState(false)
    const [failureReason, setFailureReason] = useState('')
    const webcamRef = useRef<Webcam>(null)
    const canvasRef = useRef<HTMLCanvasElement>(null)

    // Simple face detection using brightness analysis
    const detectFace = (imageData: string): Promise<boolean> => {
        if (!canvasRef.current) return Promise.resolve(false)

        const canvas = canvasRef.current
        const ctx = canvas.getContext('2d')
        if (!ctx) return Promise.resolve(false)

        const img = new Image()
        img.src = imageData

        return new Promise<boolean>((resolve) => {
            img.onload = () => {
                canvas.width = img.width
                canvas.height = img.height
                ctx.drawImage(img, 0, 0)

                // Analyze center region for face-like features
                const centerX = img.width / 2
                const centerY = img.height / 2
                const regionSize = Math.min(img.width, img.height) / 3

                const imageData = ctx.getImageData(
                    centerX - regionSize / 2,
                    centerY - regionSize / 2,
                    regionSize,
                    regionSize
                )

                let totalBrightness = 0
                let pixelCount = 0

                for (let i = 0; i < imageData.data.length; i += 4) {
                    const r = imageData.data[i]
                    const g = imageData.data[i + 1]
                    const b = imageData.data[i + 2]
                    const brightness = (r + g + b) / 3
                    totalBrightness += brightness
                    pixelCount++
                }

                const avgBrightness = totalBrightness / pixelCount

                // Face detection heuristic: center region should have moderate brightness (skin tones)
                const hasFace = avgBrightness > 60 && avgBrightness < 200
                resolve(hasFace)
            }

            img.onerror = () => resolve(false)
        })
    }

    // Compare two face images (simple similarity check)
    const compareFaces = async (enrolledFace: string, verifyFace: string): Promise<boolean> => {
        if (!canvasRef.current) return false

        const canvas = canvasRef.current
        const ctx = canvas.getContext('2d')
        if (!ctx) return false

        // Load both images
        const img1 = new Image()
        const img2 = new Image()
        img1.src = enrolledFace
        img2.src = verifyFace

        return new Promise((resolve) => {
            let loaded = 0
            const onLoad = () => {
                loaded++
                if (loaded === 2) {
                    canvas.width = 100
                    canvas.height = 100

                    ctx.drawImage(img1, 0, 0, 100, 100)
                    const data1 = ctx.getImageData(0, 0, 100, 100)

                    ctx.drawImage(img2, 0, 0, 100, 100)
                    const data2 = ctx.getImageData(0, 0, 100, 100)

                    let diff = 0
                    for (let i = 0; i < data1.data.length; i += 4) {
                        const r1 = data1.data[i]
                        const g1 = data1.data[i + 1]
                        const b1 = data1.data[i + 2]
                        const r2 = data2.data[i]
                        const g2 = data2.data[i + 1]
                        const b2 = data2.data[i + 2]

                        diff += Math.abs(r1 - r2) + Math.abs(g1 - g2) + Math.abs(b1 - b2)
                    }

                    const avgDiff = diff / (data1.data.length / 4)
                    // If average difference is less than 80, consider it a match
                    resolve(avgDiff < 80)
                }
            }

            img1.onload = onLoad
            img2.onload = onLoad
            img1.onerror = () => resolve(false)
            img2.onerror = () => resolve(false)
        })
    }

    useEffect(() => {
        if (isOpen) {
            setStep('init')
            setProgress(0)
            setCameraError(false)
            setFailureReason('')

            const timer1 = setTimeout(() => setStep('scanning'), 1500)
            return () => clearTimeout(timer1)
        }
    }, [isOpen])

    useEffect(() => {
        if (step === 'scanning') {
            const interval = setInterval(() => {
                setProgress(prev => {
                    if (prev >= 100) {
                        clearInterval(interval)
                        handleScanComplete()
                        return 100
                    }
                    return prev + 2
                })
            }, 50)
            return () => clearInterval(interval)
        }
    }, [step])

    const handleScanComplete = async () => {
        if (!webcamRef.current || cameraError) {
            setStep('success')
            setTimeout(() => onSuccess(), 1000)
            return
        }

        const imageSrc = webcamRef.current.getScreenshot()
        if (!imageSrc) {
            setFailureReason('Failed to capture image')
            setStep('failure')
            return
        }

        // Detect face in captured image
        const hasFace = await detectFace(imageSrc)
        if (!hasFace) {
            setFailureReason('No face detected. Please ensure your face is clearly visible.')
            setStep('failure')
            return
        }

        if (mode === 'enroll') {
            // Store enrolled face
            localStorage.setItem('enrolledFace', imageSrc)
            console.log('Face enrolled successfully')
            setStep('success')
            setTimeout(() => onSuccess(), 1000)
        } else {
            // Verify against enrolled face
            const enrolledFace = localStorage.getItem('enrolledFace')
            if (!enrolledFace) {
                setFailureReason('No enrolled face found. Please register first.')
                setStep('failure')
                return
            }

            const isMatch = await compareFaces(enrolledFace, imageSrc)
            if (isMatch) {
                console.log('Face verification successful')
                setStep('success')
                setTimeout(() => onSuccess(), 1000)
            } else {
                setFailureReason('Face does not match enrolled identity. Access denied.')
                setStep('failure')
            }
        }
    }

    const handleRetry = () => {
        setStep('init')
        setProgress(0)
        setFailureReason('')
        setTimeout(() => setStep('scanning'), 1500)
    }

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
            <canvas ref={canvasRef} className="hidden" />
            <div className="bg-white rounded-2xl p-8 max-w-md w-full shadow-2xl border border-gray-200">

                <div className="text-center mb-6">
                    <h2 className="text-2xl font-bold text-gray-800">
                        {mode === 'enroll' ? 'Biometric Enrollment' : 'Security Check'}
                    </h2>
                    <p className="text-gray-500">
                        {mode === 'enroll' ? 'Register your face identity' : 'Biometric Verification Required'}
                    </p>
                </div>

                {/* Camera/Scan Viewport */}
                <div className="relative w-full h-64 bg-gray-900 rounded-lg overflow-hidden flex items-center justify-center mb-6 ring-4 ring-gray-100">

                    {/* Live Webcam Feed */}
                    {(step === 'init' || step === 'scanning') && !cameraError && (
                        <Webcam
                            ref={webcamRef}
                            audio={false}
                            screenshotFormat="image/jpeg"
                            className="absolute inset-0 w-full h-full object-cover"
                            onUserMediaError={() => setCameraError(true)}
                            videoConstraints={{
                                facingMode: 'user',
                                width: 640,
                                height: 480
                            }}
                        />
                    )}

                    {/* Camera Error Fallback */}
                    {cameraError && step !== 'success' && step !== 'failure' && (
                        <div className="text-gray-400 flex flex-col items-center">
                            <Camera className="w-12 h-12 mb-2" />
                            <span className="text-sm">Camera unavailable</span>
                            <span className="text-xs text-gray-500">Using simulated mode</span>
                        </div>
                    )}

                    {step === 'init' && !cameraError && (
                        <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-30">
                            <div className="text-white flex flex-col items-center animate-pulse">
                                <Camera className="w-12 h-12 mb-2" />
                                <span>Initializing Camera...</span>
                            </div>
                        </div>
                    )}

                    {step === 'scanning' && (
                        <>
                            <div className="absolute inset-0 bg-gradient-to-b from-transparent via-blue-900/20 to-transparent animate-scan"></div>
                            <div className="absolute inset-0 border-2 border-blue-500 opacity-50 rounded-lg"></div>
                            <div
                                className="absolute top-0 left-0 w-full h-1 bg-blue-500 shadow-[0_0_15px_rgba(59,130,246,1)] transition-all duration-[50ms]"
                                style={{ top: `${progress}%` }}
                            />
                            <div className="absolute bottom-4 left-0 right-0 z-10 text-blue-400 font-mono text-sm flex flex-col items-center">
                                <Scan className="w-12 h-12 mb-2 animate-spin-slow" />
                                <span>{mode === 'enroll' ? 'Capturing Face...' : 'Verifying Identity...'} {progress}%</span>
                            </div>
                        </>
                    )}

                    {step === 'success' && (
                        <div className="text-green-500 flex flex-col items-center animate-bounce">
                            <ShieldCheck className="w-20 h-20 mb-2" />
                            <span className="text-xl font-bold">
                                {mode === 'enroll' ? 'Identity Registered' : 'Identity Verified'}
                            </span>
                        </div>
                    )}

                    {step === 'failure' && (
                        <div className="text-red-500 flex flex-col items-center">
                            <ShieldAlert className="w-20 h-20 mb-2" />
                            <span className="text-xl font-bold">Verification Failed</span>
                        </div>
                    )}

                </div>

                <div className="text-center">
                    {step === 'scanning' && (
                        <p className="text-sm text-gray-400">Please look directly at the camera</p>
                    )}
                    {step === 'success' && (
                        <p className="text-sm text-green-600">
                            {mode === 'enroll' ? 'Profile saved successfully.' : 'Access Granted. Decrypting...'}
                        </p>
                    )}
                    {step === 'failure' && (
                        <div className="space-y-2">
                            <p className="text-sm text-red-600">{failureReason}</p>
                            <button
                                onClick={handleRetry}
                                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 text-sm font-medium"
                            >
                                Try Again
                            </button>
                        </div>
                    )}
                </div>

                {step !== 'failure' && (
                    <button
                        onClick={onClose}
                        className="mt-6 w-full py-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 text-sm font-medium"
                    >
                        Cancel
                    </button>
                )}

            </div>
        </div>
    )
}
