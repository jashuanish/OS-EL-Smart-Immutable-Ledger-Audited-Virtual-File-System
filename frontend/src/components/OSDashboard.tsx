'use client'

import React, { useState, useEffect } from 'react'

interface Process {
    pid: number
    user_id: string
    name: string
    state: string
    priority: number
    cpu_time: number
    memory_usage: number
    logs: string[]
}

interface Stats {
    memory: {
        total: number
        used_frames: number
        page_faults: number
    }
    disk: {
        head_pos: number
        total_movement: number
    }
    scheduler: {
        algo: string
        queue_size: number
    }
}

export default function OSDashboard() {
    const [processes, setProcesses] = useState<Process[]>([])
    const [stats, setStats] = useState<Stats | null>(null)
    const [selectedAlgo, setSelectedAlgo] = useState<string>('FCFS')
    const [loading, setLoading] = useState(true)

    const fetchData = async () => {
        try {
            const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
            const procRes = await fetch(`${baseUrl}/api/v1/os/processes`)
            const statsRes = await fetch(`${baseUrl}/api/v1/os/stats`)

            const procs = await procRes.json()
            const st = await statsRes.json()

            setProcesses(procs)
            setStats(st)
            if (st && st.scheduler) {
                setSelectedAlgo(st.scheduler.algo)
            }
        } catch (e) {
            console.error("Failed to fetch OS data", e)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchData()
        const interval = setInterval(fetchData, 500)
        return () => clearInterval(interval)
    }, [])

    const changeScheduler = async (algo: string) => {
        const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        await fetch(`${baseUrl}/api/v1/os/scheduler/${algo}`, { method: 'POST' })
        fetchData()
    }

    if (loading && !stats) return <div className="p-8">Loading Kernel...</div>

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pb-20">

            {/* CPU / Scheduler */}
            <div className="bg-white p-6 rounded-xl shadow-sm border">
                <h2 className="text-lg font-bold mb-4 flex items-center">
                    <span className="text-2xl mr-2">⚙️</span> CPU Scheduler
                </h2>
                <div className="flex gap-2 mb-4">
                    {['FCFS', 'SJF', 'PRIORITY', 'ROUND_ROBIN'].map(algo => (
                        <button
                            key={algo}
                            onClick={() => changeScheduler(algo)}
                            className={`px-3 py-1 rounded text-xs font-bold ${selectedAlgo === algo ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'}`}
                        >
                            {algo}
                        </button>
                    ))}
                </div>
                <div className="grid grid-cols-2 gap-4 text-sm">
                    <div className="bg-gray-50 p-3 rounded">
                        <div className="text-gray-500">Current Algorithm</div>
                        <div className="font-mono text-lg">{stats?.scheduler.algo}</div>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                        <div className="text-gray-500">Ready Queue</div>
                        <div className="font-mono text-lg">{stats?.scheduler.queue_size} Processes</div>
                    </div>
                </div>
            </div>

            {/* Memory / Disk */}
            <div className="bg-white p-6 rounded-xl shadow-sm border">
                <h2 className="text-lg font-bold mb-4 flex items-center">
                    <span className="text-2xl mr-2">💾</span> Memory & I/O
                </h2>

                <div className="space-y-4">
                    <div>
                        <div className="flex justify-between text-xs mb-1">
                            <span>RAM Usage ({stats?.memory.used_frames} Frames)</span>
                            <span>1MB Total</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2.5">
                            <div
                                className="bg-green-600 h-2.5 rounded-full transition-all duration-500"
                                style={{ width: `${Math.min(((stats?.memory.used_frames || 0) * 4 / 1024) * 100, 100)}%` }}></div>
                        </div>
                        <div className="text-xs text-red-500 mt-1">Page Faults: {stats?.memory.page_faults}</div>
                    </div>

                    <div className="border-t pt-4">
                        <div className="flex justify-between text-sm">
                            <span>Disk Head Position:</span>
                            <span className="font-mono">{stats?.disk.head_pos} / 1000</span>
                        </div>
                        <div className="flex justify-between text-sm">
                            <span>Total Seek Movement:</span>
                            <span className="font-mono">{stats?.disk.total_movement}</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Process Table */}
            <div className="bg-white p-6 rounded-xl shadow-sm border lg:col-span-2">
                <h2 className="text-lg font-bold mb-4">Process Table</h2>
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">PID</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">State</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Mem</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Activity</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {processes.length === 0 ? (
                                <tr><td colSpan={5} className="px-6 py-4 text-center text-sm text-gray-500">No active processes</td></tr>
                            ) : (
                                processes.map(proc => (
                                    <tr key={proc.pid}>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{proc.pid}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{proc.name}</td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                                        ${proc.state === 'RUNNING' ? 'bg-green-100 text-green-800' :
                                                    proc.state === 'WAITING' ? 'bg-yellow-100 text-yellow-800' :
                                                        proc.state === 'READY' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}`}>
                                                {proc.state}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{proc.memory_usage} frames</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-xs text-gray-400 font-mono">
                                            {proc.logs && proc.logs.length > 0 ? proc.logs[proc.logs.length - 1].split(']').pop() : '-'}
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

        </div>
    )
}
