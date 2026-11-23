/* Cầu nối giữa các track (master 7.4). Cấu trúc ở đây; văn bản ở shared/bridges.{vi,en}.js (khoá shared.bridge.<id>.*).
   owner = chương chủ sở hữu (viết đầy đủ một lần); links = nơi chỉ tóm tắt 1–2 dòng kèm link.
   Tham chiếu tới track chưa đăng ký chỉ bị cảnh báo (không phải lỗi) cho tới khi track đó được thêm. */
ADE.addBridges([
  { id: 'X1', owner: 'runtime/b7', links: ['animation/c1', 'animation/c5', 'animation/c7', 'ui/e9'] },
  { id: 'X2', owner: 'coroutines/a8', links: ['runtime/b4', 'runtime/b8', 'animation/c6'] },
  { id: 'X3', owner: 'runtime/b5', links: ['animation/c7', 'coroutines/a4'] },
  { id: 'X4', owner: 'animation/c6', links: ['coroutines/a5', 'coroutines/a2'] },
  { id: 'X5', owner: 'ui/e8', links: ['ui/e2', 'ui/e3', 'runtime/b0'] },
  { id: 'X6', owner: 'ui/e10', links: ['runtime/b9', 'ux/d2', 'ux/d9'] },
  { id: 'X7', owner: 'ui/e9', links: ['animation/c0', 'animation/c2', 'ux/d1'] },
  { id: 'X8', owner: 'ux/d9', links: ['ui/e7'] },
  { id: 'X9', owner: 'kotlin/k8', links: ['coroutines/a8'] },
  { id: 'X10', owner: 'kotlin/k10', links: ['coroutines/fl'] },
  { id: 'X11', owner: 'kotlin/k11', links: ['runtime/b4'] },
  { id: 'X12', owner: 'arch/g3', links: ['coroutines/a8', 'runtime/sh'] }
]);
