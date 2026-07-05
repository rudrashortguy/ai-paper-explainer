import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

export default function Uploader({ onUpload }) {
  const onDrop = useCallback(
    (files) => {
      if (files?.[0]) onUpload(files[0]);
    },
    [onUpload],
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-xl p-16 text-center cursor-pointer transition-colors ${
        isDragActive
          ? 'border-blue-400 bg-blue-900/30'
          : 'border-white/20 hover:border-white/40'
      }`}
    >
      <input {...getInputProps()} />
      <p className="text-xl">
        {isDragActive
          ? 'Drop your PDF here'
          : 'Drag & drop a research paper, or click to select'}
      </p>
    </div>
  );
}
