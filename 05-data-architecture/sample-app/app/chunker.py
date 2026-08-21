"""Chunking strategies for document processing."""
import re
from typing import Optional


def fixed_chunking(text: str, chunk_size: int = 500, overlap: int = 50) -> list[dict]:
    """
    Split text into fixed-size chunks with overlap.
    
    Args:
        text: Input text
        chunk_size: Maximum characters per chunk
        overlap: Overlap between chunks
        
    Returns:
        List of chunk dictionaries
    """
    chunks = []
    start = 0
    chunk_index = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end]
        
        chunks.append({
            "text": chunk_text,
            "chunk_index": chunk_index,
            "token_count": len(chunk_text.split()),
            "strategy": "fixed"
        })
        
        chunk_index += 1
        start = end - overlap
    
    return chunks


def semantic_chunking(text: str) -> list[dict]:
    """
    Split text by semantic boundaries (paragraphs, sentences).
    
    Args:
        text: Input text
        
    Returns:
        List of chunk dictionaries
    """
    chunks = []
    
    paragraphs = re.split(r'\n\s*\n', text)
    
    current_chunk = ""
    chunk_index = 0
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        
        if len(current_chunk) + len(paragraph) < 1000:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk:
                chunks.append({
                    "text": current_chunk.strip(),
                    "chunk_index": chunk_index,
                    "token_count": len(current_chunk.split()),
                    "strategy": "semantic"
                })
                chunk_index += 1
            
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk) + len(sentence) < 500:
                    current_chunk += sentence + " "
                else:
                    if current_chunk:
                        chunks.append({
                            "text": current_chunk.strip(),
                            "chunk_index": chunk_index,
                            "token_count": len(current_chunk.split()),
                            "strategy": "semantic"
                        })
                        chunk_index += 1
                    current_chunk = sentence + " "
    
    if current_chunk.strip():
        chunks.append({
            "text": current_chunk.strip(),
            "chunk_index": chunk_index,
            "token_count": len(current_chunk.split()),
            "strategy": "semantic"
        })
    
    return chunks


def structure_aware_chunking(text: str) -> list[dict]:
    """
    Split text by document structure (headings, sections).
    
    Args:
        text: Input text
        
    Returns:
        List of chunk dictionaries
    """
    chunks = []
    
    sections = re.split(r'\n(?=#{1,3}\s)', text)
    
    chunk_index = 0
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        heading_match = re.match(r'^(#{1,3})\s+(.+)', section)
        
        if heading_match:
            if len(section) > 1500:
                subsections = re.split(r'\n(?=#{2,4}\s)', section)
                for subsection in subsections:
                    subsection = subsection.strip()
                    if subsection:
                        chunks.append({
                            "text": subsection,
                            "chunk_index": chunk_index,
                            "token_count": len(subsection.split()),
                            "strategy": "structure",
                            "heading": heading_match.group(2) if heading_match else None
                        })
                        chunk_index += 1
            else:
                chunks.append({
                    "text": section,
                    "chunk_index": chunk_index,
                    "token_count": len(section.split()),
                    "strategy": "structure",
                    "heading": heading_match.group(2)
                })
                chunk_index += 1
        else:
            if len(section) > 1000:
                paragraphs = re.split(r'\n\s*\n', section)
                current_chunk = ""
                
                for paragraph in paragraphs:
                    if len(current_chunk) + len(paragraph) < 1000:
                        current_chunk += paragraph + "\n\n"
                    else:
                        if current_chunk:
                            chunks.append({
                                "text": current_chunk.strip(),
                                "chunk_index": chunk_index,
                                "token_count": len(current_chunk.split()),
                                "strategy": "structure"
                            })
                            chunk_index += 1
                        current_chunk = paragraph + "\n\n"
                
                if current_chunk.strip():
                    chunks.append({
                        "text": current_chunk.strip(),
                        "chunk_index": chunk_index,
                        "token_count": len(current_chunk.split()),
                        "strategy": "structure"
                    })
                    chunk_index += 1
            else:
                chunks.append({
                    "text": section,
                    "chunk_index": chunk_index,
                    "token_count": len(section.split()),
                    "strategy": "structure"
                })
                chunk_index += 1
    
    return chunks


def chunk_document(
    text: str,
    strategy: str = "fixed",
    chunk_size: int = 500,
    overlap: int = 50
) -> list[dict]:
    """
    Chunk a document using the specified strategy.
    
    Args:
        text: Input text
        strategy: Chunking strategy (fixed, semantic, structure)
        chunk_size: Chunk size for fixed strategy
        overlap: Overlap for fixed strategy
        
    Returns:
        List of chunk dictionaries
    """
    if strategy == "fixed":
        return fixed_chunking(text, chunk_size, overlap)
    elif strategy == "semantic":
        return semantic_chunking(text)
    elif strategy == "structure":
        return structure_aware_chunking(text)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
