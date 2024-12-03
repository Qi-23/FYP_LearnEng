import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.css';
import Link from 'next/link';
import ReactDOM from "react-dom/client";

export default function Home() {
  return (
    <div className='text-center mt-5'>
      <Link href="/scenario_configuration" className='link'>Scenario Configuration Page</Link>
      <br/>
      <Link href="/character" className='link'>Character Page</Link>
      <br/>
      <Link href="/chatting" className='link'>Chatting Page</Link>
      <br/>
      <Link href="/scenario" className='link'>Scenario Page</Link>
      <br />
      <Link href="/testing" className='link'>Testing Page</Link>
      <br />
      <a href="/chatting" className='link'>Chatting html</a>
    </div>
    
  )
}
