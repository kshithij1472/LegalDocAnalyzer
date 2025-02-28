import React, { useState, useContext } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';
import { ArrowUpTrayIcon, DocumentTextIcon } from '@heroicons/react/24/outline';

const Analyzer = () => {
    const { user } = useAuth();
    const [file, setFile] = useState(null);
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleFileUpload = async (files) => {
        setError('');
        setFile(files[0]);
    };

    const analyzeDocument = async () => {
        if (!file || !user) return;
        
        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('/analyze', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Bearer ${user.token}`
                }
            });
            
            setResults(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Analysis failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const highlightEntities = (text, entities) => {
        let lastIndex = 0;
        const elements = [];
        
        entities.sort((a, b) => a.start - b.start).forEach(entity => {
            // Add text before entity
            elements.push(text.slice(lastIndex, entity.start));
            
            // Add highlighted entity
            elements.push(
                <span key={`${entity.start}-${entity.end}`} 
                      className={`entity-tag ${entity.label.toLowerCase()}`}>
                    {text.slice(entity.start, entity.end)}
                    <span className="entity-label">{entity.label}</span>
                </span>
            );
            
            lastIndex = entity.end;
        });
        
        // Add remaining text
        elements.push(text.slice(lastIndex));
        return elements;
    };

    return (
        <div className="max-w-4xl mx-auto p-6">
            <div className="bg-white rounded-lg shadow-md p-8 mb-8">
                <h1 className="text-3xl font-bold text-legal-primary mb-6">
                    <DocumentTextIcon className="h-8 w-8 inline-block mr-3" />
                    Legal Document Analyzer
                </h1>
                
                <div className={`border-2 border-dashed rounded-xl p-8 text-center 
                               ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}>
                    <input
                        type="file"
                        onChange={(e) => handleFileUpload(e.target.files)}
                        accept=".pdf,.docx"
                        className="hidden"
                        id="file-upload"
                        disabled={loading}
                    />
                    <label
                        htmlFor="file-upload"
                        className="cursor-pointer inline-block"
                    >
                        <div className="mb-4 text-gray-600">
                            <ArrowUpTrayIcon className="h-12 w-12 mx-auto" />
                            <p className="mt-2">
                                {file ? file.name : 'Drag & drop or click to upload'}
                            </p>
                        </div>
                    </label>
                    
                    <button
                        onClick={analyzeDocument}
                        disabled={!file || loading}
                        className="bg-legal-primary text-white px-8 py-3 rounded-lg
                                 hover:bg-legal-secondary transition-colors
                                 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {loading ? 'Analyzing...' : 'Analyze Document'}
                    </button>
                </div>

                {error && (
                    <div className="mt-4 p-4 bg-red-100 text-red-700 rounded-lg">
                        {error}
                    </div>
                )}

                {results && (
                    <div className="mt-8 space-y-8">
                        <div className="bg-gray-50 p-6 rounded-lg">
                            <h2 className="text-xl font-semibold mb-4">Identified Entities</h2>
                            <div className="flex flex-wrap gap-2 mb-4">
                                {results.entities.map((entity, index) => (
                                    <span 
                                        key={index}
                                        className={`px-3 py-1 rounded-full text-sm
                                            ${entity.label === 'PARTY' ? 
                                              'bg-blue-100 text-blue-800' :
                                              entity.label === 'CLAUSE' ? 
                                              'bg-green-100 text-green-800' :
                                              'bg-yellow-100 text-yellow-800'}`
                                        }
                                    >
                                        {entity.text} ({entity.label})
                                    </span>
                                ))}
                            </div>
                        </div>

                        <div className="bg-gray-50 p-6 rounded-lg">
                            <h2 className="text-xl font-semibold mb-4">Simplified Document</h2>
                            <div className="prose max-w-none">
                                {highlightEntities(results.original_text, results.entities)}
                            </div>
                        </div>

                        <div className="bg-gray-50 p-6 rounded-lg">
                            <h2 className="text-xl font-semibold mb-4">Simplified Explanation</h2>
                            <p className="whitespace-pre-wrap text-gray-700">
                                {results.simplified_text}
                            </p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Analyzer;