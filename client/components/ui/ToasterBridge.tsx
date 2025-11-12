"use client";
import * as React from "react";
import { ToastContainer } from "./Toast";
import { useToastStore } from "@/lib/stores/toastStore";

export default function ToasterBridge() {
  const { messages, remove } = useToastStore();
  return <ToastContainer messages={messages} onRemove={remove} />;
}
